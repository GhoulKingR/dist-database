from customer import id_to_code, count_customers, create_app
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
def customerdb():
    try:
        conn = sqlite3.connect("databases/grp9customer.db")
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

def test_get_all(client, customerdb):
    response = client.get("/api/customers")
    assert len(response.json) == count_customers(customerdb)

def test_wrong_call_fails(client):
    response = client.get("/api/customers/233")
    assert response.status_code == 404

def test_right_is_successful(client):
    response = client.get("/api/customers/C00001")
    assert response.json["code"] == "C00001"

def test_can_create_customer(client):
    response = client.post("/api/customers", json={
        "name": "Chigozie Oduah",
        "city": "Ladilak",
        "working_area": "Lagos",
        "country": "Nigeria",
        "grade": 5,
        "opening_amt": 100.00,
        "receive_amt": 200.00,
        "payment_amt": 20000.00,
        "outstanding_amt": 0.00,
        "phone_no": "01234959882",
        "agent_code": "A002",
    })
    assert response.status_code == 200

def test_missing_args_fail(client):
    response = client.post("/api/customers", json={
        "name": "Chigozie Oduah",
        "working_area": "Tenesse",
        "phone_no": "077-02346674",
    })
    assert response.status_code == 400

def test_can_delete(client):
    delete_resp = client.delete("/api/customers/C00013")
    assert delete_resp.status_code == 200
    resp = client.get("/api/customers/C00013")
    assert resp.status_code == 404

def test_can_update(client):
    update_resp = client.put("/api/customers/C00003", json={
        "name": "Chigozie",
    })
    assert update_resp.status_code == 200
    resp = client.get("/api/customers/C00003")
    assert resp.json["name"] == "Chigozie"

def test_new_id():
    assert id_to_code(3) == "C00003"

def test_works_on_gt_5():
    assert id_to_code(1234567) == "C1234567"