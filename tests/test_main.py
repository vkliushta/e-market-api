import pytest


@pytest.mark.anyio
async def test_root(async_test_client):
    response = await async_test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello Bigger Applications!"}
