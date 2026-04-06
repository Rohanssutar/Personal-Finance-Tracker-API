def test_create_user(client):
    response = client.post("/users/", json={
        "username": "rohan",
        "email": "rohan@example.com",
        "password": "password1234",
        "role": "viewer"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "rohan"
    assert data["email"] == "rohan@example.com"
    assert "id" in data


def test_get_user(client):
    create_response = client.post("/users/", json={
        "username": "john",
        "email": "john@example.com",
        "password": "password123456",
        "role": "analyst"
    })
    user_id = create_response.json()["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["username"] == "john"


def test_update_user(client):
    create_response = client.post("/users/", json={
        "username": "john",
        "email": "john@example.com",
        "password": "password1234",
        "role": "analyst"
    })
    user_id = create_response.json()["id"]

    response = client.put(f"/users/{user_id}", json={
        "username": "charlie",
        "email": "charlie@example.com",
        "password": "charlie1234",
        "role": "admin"
    })
    assert response.status_code == 200
    assert response.json()["username"] == "charlie"
    assert response.json()["role"] == "admin"


def test_delete_user(client):
    create_response = client.post("/users/", json={
        "username": "john",
        "email": "john@example.com",
        "password": "password1234",
        "role": "analyst"
    })
    user_id = create_response.json()["id"]

    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200

    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 404

