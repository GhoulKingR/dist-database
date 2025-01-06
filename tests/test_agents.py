def test_get_all(client):
    response = client.get("/api/agents")
    print(response)
    assert len(response.json) == 12

def test_wrong_call_fails(client):
    response = client.get("/api/agents/233")
    assert response.status_code == 404

def test_right_is_successful(client):
    response = client.get("/api/agents/A002")
    assert response.status_code == 200
