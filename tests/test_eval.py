from fastapi.testclient import TestClient
from selfrag.main import app

client = TestClient(app)


def test_pass_and_fail():
    good = client.post("/evaluate", json={"answer": 'The platform refuses latest tags.', "gold": 'The platform refuses latest tags.', "context": 'The platform refuses latest tags in production.'}).json()
    assert good["passed"] is True
    bad = client.post("/evaluate", json={"answer": "The cafeteria serves soup.", "gold": 'The platform refuses latest tags.', "context": 'The platform refuses latest tags in production.'}).json()
    assert bad["passed"] is False
