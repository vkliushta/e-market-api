def test_create_user(test_client, cleanup_db_users_table):
    response = test_client.post(
        "users/",
        json={"email": "random_email@mail.com", "password": "dummy_password"},
    )
    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "email": "random_email@mail.com",
        "is_active": True,
        "items": [],
    }
    response = test_client.post(
        "users/",
        json={"email": "random_email@mail.com", "password": "dummy_password"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}


def test_read_users(test_client, fill_db_users_table, cleanup_db_users_table):
    response = test_client.get("users/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "email": "random_email@mail.com",
            "is_active": True,
            "items": [],
        },
    ]


def test_read_user(test_client, fill_db_users_table, cleanup_db_users_table):
    response = test_client.get("users/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "email": "random_email@mail.com",
        "is_active": True,
        "items": [],
    }
    response = test_client.get("users/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
