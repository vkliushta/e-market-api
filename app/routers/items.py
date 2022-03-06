from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import schemas
from ..crud import items
from ..database import get_db

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    all_items = items.get_items(db, skip=skip, limit=limit)
    return all_items


@router.post("/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int,
    item: schemas.ItemCreate,
    db: Session = Depends(get_db),
):
    return items.create_user_item(db=db, item=item, user_id=user_id)
