from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_signup_updates_activity_participants_immediately():
    activity_name = "Chess Club"
    email = "freshsignon@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200

    response = client.get("/activities")
    assert response.status_code == 200
    assert email in response.json()[activity_name]["participants"]

    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    assert response.status_code == 200


def test_unregister_participant_removes_student_from_activity():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200

    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    assert response.status_code == 200
    assert email not in response.json()["participants"]

    response = client.get("/activities")
    assert response.status_code == 200
    assert email not in response.json()[activity_name]["participants"]


def test_unregister_participant_returns_404_for_missing_activity():
    response = client.delete("/activities/Unknown Activity/unregister?email=test@mergington.edu")
    assert response.status_code == 404


def test_unregister_participant_returns_400_when_student_not_signed_up():
    activity_name = "Basketball Team"
    email = "notregistered@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    assert response.status_code == 400
