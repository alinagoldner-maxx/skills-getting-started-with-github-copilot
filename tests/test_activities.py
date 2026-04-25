"""Integration tests for FastAPI activities endpoints using AAA pattern"""


def test_get_all_activities(client, reset_activities):
    # Arrange
    expected_activity_count = 2
    
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    assert response.status_code == 200
    assert len(data) == expected_activity_count
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_get_activities_returns_correct_structure(client, reset_activities):
    # Arrange - activity structure definition
    required_fields = {"description", "schedule", "max_participants", "participants"}
    
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    assert response.status_code == 200
    for activity_name, activity_data in data.items():
        assert set(activity_data.keys()) == required_fields


def test_signup_for_activity_success(client, reset_activities):
    # Arrange
    activity_name = "Chess Club"
    email = "charlie@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    data = response.json()
    
    # Assert
    assert response.status_code == 200
    assert "Signed up" in data["message"]
    
    # Verify participant was added
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert email in activities_data["Chess Club"]["participants"]


def test_signup_activity_not_found(client, reset_activities):
    # Arrange
    activity_name = "NonexistentActivity"
    email = "charlie@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    data = response.json()
    
    # Assert
    assert response.status_code == 404
    assert data["detail"] == "Activity not found"


def test_signup_duplicate_student(client, reset_activities):
    # Arrange
    activity_name = "Chess Club"
    email = "alice@mergington.edu"  # Already signed up
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    data = response.json()
    
    # Assert
    assert response.status_code == 400
    assert "already signed up" in data["detail"]


def test_unregister_success(client, reset_activities):
    # Arrange
    activity_name = "Chess Club"
    email = "alice@mergington.edu"  # Already in participants
    
    # Act
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    data = response.json()
    
    # Assert
    assert response.status_code == 200
    assert "Unregistered" in data["message"]
    
    # Verify participant was removed
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert email not in activities_data["Chess Club"]["participants"]


def test_unregister_activity_not_found(client, reset_activities):
    # Arrange
    activity_name = "NonexistentActivity"
    email = "alice@mergington.edu"
    
    # Act
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    data = response.json()
    
    # Assert
    assert response.status_code == 404
    assert data["detail"] == "Activity not found"


def test_unregister_student_not_in_activity(client, reset_activities):
    # Arrange
    activity_name = "Chess Club"
    email = "bob@mergington.edu"  # Not in Chess Club
    
    # Act
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    data = response.json()
    
    # Assert
    assert response.status_code == 400
    assert "not signed up" in data["detail"]
