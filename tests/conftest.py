import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models
from app.database import Base, get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
async def async_test_client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def test_client():
    yield TestClient(app)


def cleanup_db_table(model):
    db = TestingSessionLocal()
    db.query(model).delete()
    db.commit()


@pytest.fixture
def cleanup_db_items_table():
    yield
    cleanup_db_table(models.Item)


@pytest.fixture
def fill_db_items_table():
    db = TestingSessionLocal()
    db_item = models.Item(
        title="dummy_title",
        description="random description",
        owner_id=1,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)


@pytest.fixture
def cleanup_db_users_table():
    yield
    cleanup_db_table(models.User)


@pytest.fixture
def fill_db_users_table():
    db = TestingSessionLocal()
    db_user = models.User(
        email="random_email@mail.com",
        hashed_password="fake_hashed_password",
        is_active=True,
        items=[],
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
