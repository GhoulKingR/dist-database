from order import id_to_code, count_orders, create_app
import pytest
import sqlite3

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True
    })

    yield app

@pytest.fixture
def database():
    conn = None
    try:
        conn = sqlite3.connect("databases/grp9order.db")
        yield conn

    except sqlite3.Error as err:
        print("An SQL error occured:", err)
        return {}, 500  # internal server error
    
    finally:
        if conn:
            conn.close()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

def test_get_all(client, database):
    response = client.get("/api/orders")
    assert len(response.json) == count_orders(database)

def test_wrong_call_fails(client):
    response = client.get("/api/orders/233")
    assert response.status_code == 404

def test_right_is_successful(client):
    response = client.get("/api/orders/200100")
    assert response.json["num"] == 200100

def test_can_create_customer(client):
    response = client.post("/api/orders", json={
        "amount": '40000.12',
        "advance_amount": '1200.21',
        "ord_date": '8/12/2005',
        "cust_code": 'C0001',
        "agent_code": 'A007',
        "description": 'SOD',
    })
    assert response.status_code == 200

def test_missing_args_fail(client):
    response = client.post("/api/orders", json={
        "num": 2100.00,
        "cust_code": "C00003",
    })
    assert response.status_code == 400

def test_can_delete(client):
    delete_resp = client.delete("/api/orders/200110")
    assert delete_resp.status_code == 200
    resp = client.get("/api/orders/200110")
    assert resp.status_code == 404

def test_can_update(client):
    update_resp = client.put("/api/orders/200100", json={
        "amount": 2100.00,
    })
    assert update_resp.status_code == 200
    resp = client.get("/api/orders/200100")
    assert resp.status_code == 200
    assert resp.json["amount"] == 2100.00

def test_new_id():
    assert id_to_code(3) == str(200100 + 3)

def test_works_on_gt_5():
    assert id_to_code(1234567) == str(200100 + 1234567)
