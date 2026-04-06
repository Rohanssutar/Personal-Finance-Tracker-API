def test_create_transaction(client, admin_user):
    response = client.post(
        f"/transactions/?user_id={admin_user.id}",
        json={
            "amount": 150.50,
            "type": "expense",
            "category": "grocery",
            "description": "Weekly groceries",
            "date": "2026-04-06"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["amount"] == 150.50
    assert data["category"] == "grocery"


def test_get_all_transactions(client, admin_user):
    client.post(
        f"/transactions/?user_id={admin_user.id}",
        json={
            "amount": 100,
            "type": "expense",
            "category": "travel",
            "description": "Bus ticket",
            "date": "2026-04-06"
        }
    )
    response = client.get(f"/transactions/?user_id={admin_user.id}")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_update_transaction(client, admin_user):
    create_response = client.post(
        f"/transactions/?user_id={admin_user.id}",
        json={
            "amount": 1550,
            "type": "expense",
            "category": "shopping",
            "description": "Shoes",
            "date": "2026-04-06"
        })
    tx_id = create_response.json()["id"]

    update_respone = client.put(
        f"/transactions/{tx_id}?user_id={admin_user.id}",
        json={
            "amount": 2000,
            "type": "expense",
            "category": "shopping",
            "description": "Adidas Shoes",
            "date": "2026-04-06"
        })
    assert update_respone.status_code == 200
    assert update_respone.json()["amount"] == 2000
    assert update_respone.json()["description"] == "Adidas Shoes"


def test_delete_transaction(client, admin_user):
    create_response = client.post(
        f"/transactions/?user_id={admin_user.id}",
        json={
            "amount": 100,
            "type": "expense",
            "category": "shopping",
            "description": "T-shirt",
            "date": "2026-04-06"
        })
    tx_id = create_response.json()["id"]

    delete_response = client.delete(f"/transactions/{tx_id}?user_id={admin_user.id}")
    assert delete_response.status_code == 200

    get_response = client.get(f"/transactions/{tx_id}?user_id={admin_user.id}")
    assert get_response.status_code == 404


def test_financial_summary(client, admin_user):
    client.post(
        f"/transactions/?user_id={admin_user.id}",
        json={
            "amount": 5000,
            "type": "income",
            "category": "job",
            "description": "Salary",
            "date": "2026-04-01"
        })
    
    client.post(
        f"/transactions/?user_id={admin_user.id}",
        json={
            "amount": 1000,
            "type": "expense",
            "category": "grocery",
            "description": "Fruits and Vegetable",
            "date": "2026-04-05"
        })
    
    response = client.get(f"/transactions/summary?user_id={admin_user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["total_income"] == 5000
    assert data["total_expenses"] == 1000
    assert data["balance"] == 4000


def test_category_wise_breakdown(client, admin_user):
    client.post(
        f"/transactions/?user_id={admin_user.id}",
        json={
            "amount": 50,
            "type": "expense",
            "category": "grocery",
            "description": "Milk",
            "date": "2026-04-01"
        })
    
    client.post(
        f"/transactions/?user_id={admin_user.id}",
        json={
            "amount": 500,
            "type": "expense",
            "category": "grocery",
            "description": "Vegetables",
            "date": "2026-04-01"
        })
    
    client.post(
        f"/transactions/?user_id={admin_user.id}",
        json={
            "amount": 5000,
            "type": "expense",
            "category": "travel",
            "description": "School trip",
            "date": "2026-04-01"
        })
    
    response = client.get(f"/transactions/category-wise-breakdown?user_id={admin_user.id}")
    assert response.status_code == 200
    data = response.json()

    grocery_data = next((item for item in data if item["category"] == "grocery"), None)
    travel_data = next((item for item in data if item["category"] == "travel"), None)

    assert grocery_data["total_expense"] == 550
    assert travel_data["total_expense"] == 5000