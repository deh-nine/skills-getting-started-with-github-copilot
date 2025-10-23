import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_for_activity():
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Remove if already present
    client.delete(f"/activities/{activity}/participants/{email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"
    # Try duplicate signup
    response_dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert response_dup.status_code == 400
    # Remove participant
    response_del = client.delete(f"/activities/{activity}/participants/{email}")
    assert response_del.status_code == 200
    assert response_del.json()["message"] == f"Removed {email} from {activity}"
    # Remove non-existent participant
    response_del2 = client.delete(f"/activities/{activity}/participants/{email}")
    assert response_del2.status_code == 404


def test_signup_invalid_activity():
    response = client.post("/activities/NonexistentActivity/signup?email=someone@mergington.edu")
    assert response.status_code == 404


def test_remove_invalid_activity():
    response = client.delete("/activities/NonexistentActivity/participants/someone@mergington.edu")
    assert response.status_code == 404


def test_remove_invalid_participant():
    response = client.delete("/activities/Chess Club/participants/notfound@mergington.edu")
    assert response.status_code == 404
