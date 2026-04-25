"""Pytest configuration and fixtures for FastAPI test suite"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Fixture providing a TestClient connected to the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Fixture to reset activities to fresh test data before each test"""
    original_activities = activities.copy()
    
    # Clear and reset with fresh test data
    activities.clear()
    activities.update({
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["alice@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["bob@mergington.edu"]
        }
    })
    
    yield activities
    
    # Restore original activities after test
    activities.clear()
    activities.update(original_activities)
