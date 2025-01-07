from agents import id_to_code, count_agents

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

def test_new_id():
    assert id_to_code(3) == "A003"

def test_works_on_gt_4():
    assert id_to_code(2000) == "A2000"