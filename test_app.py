from fastapi.testclient import TestClient

from app.app import app

client = TestClient(app)

def test_auth():
    resp= client.request("post", '/auth', {"email": "clschalkwyk@gmail.com", "password":"123"})
    assert resp.status_code == 200