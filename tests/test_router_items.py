def test_create_item_for_user(test_client, cleanup_db_items_table):
    response = test_client.post(
        "/items/22/items",
        json={"title": "dummy_title", "description": "random description"},
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "title": "dummy_title",
        "description": "random description",
        "owner_id": 22,
    }


def test_read_items(test_client, fill_db_items_table, cleanup_db_items_table):
    response = test_client.get("/items")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "title": "dummy_title",
            "description": "random description",
            "owner_id": 1,
        },
    ]
