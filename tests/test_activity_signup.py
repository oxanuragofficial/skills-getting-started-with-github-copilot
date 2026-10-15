from fastapi.testclient import TestClient

from src import app as app_module


def test_signup_updates_activity_list(monkeypatch):
    # Arrange
    activity_name = "Test Activity"
    email = "student@mergington.edu"
    monkeypatch.setitem(
        app_module.activities,
        activity_name,
        {
            "description": "Activity used to test signups",
            "schedule": "Fridays",
            "max_participants": 2,
            "participants": [],
        },
    )
    client = TestClient(app_module.app)

    # Act
    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    activities_response = client.get("/activities")

    # Assert
    assert signup_response.status_code == 200
    assert signup_response.json() == {
        "message": f"Signed up {email} for {activity_name}"
    }
    assert activities_response.status_code == 200
    assert email in activities_response.json()[activity_name]["participants"]
