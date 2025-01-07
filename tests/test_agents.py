from agents import id_to_code, count_agents
from agents import create_app
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
def agentdb():
    try:
        conn = sqlite3.connect("databases/grp9agents.db")
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

def test_get_all(client, agentdb):
    response = client.get("/api/agents")
    assert len(response.json) == count_agents(agentdb)

def test_wrong_call_fails(client):
    response = client.get("/api/agents/233")
    assert response.status_code == 404

def test_right_is_successful(client):
    response = client.get("/api/agents/A002")
    assert response.json["code"] == "A002"

def test_can_create_agent(client):
    response = client.post("/api/agents", json={
        "name": "Chigozie Oduah",
        "working_area": "Tenesse",
        "commission": "0.50",
        "phone_no": "077-02346674",
        "country": "",
    })
    assert response.status_code == 200

def test_missing_args_fail(client):
    response = client.post("/api/agents", json={
        "name": "Chigozie Oduah",
        "working_area": "Tenesse",
        "commission": "0.50",
        "phone_no": "077-02346674",
    })
    assert response.status_code == 400

def test_can_delete(client):
    delete_resp = client.delete("/api/agents/A002")
    assert delete_resp.status_code == 200
    resp = client.get("/api/agents/A002")
    assert resp.status_code == 404

def test_can_update(client):
    update_resp = client.put("/api/agents/A003", json={
        "name": "Chigozie",
    })
    assert update_resp.status_code == 200
    resp = client.get("/api/agents/A003")
    assert resp.json["name"] == "Chigozie"

def test_new_id():
    assert id_to_code(3) == "A003"

def test_works_on_gt_4():
    assert id_to_code(2000) == "A2000"