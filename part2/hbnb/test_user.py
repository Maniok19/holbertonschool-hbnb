import pytest
import requests
import json

BASE_URL = "http://localhost:5000/api/v1/users"
USER_ID = None  # To store the created user's ID for later tests

# Fixture to create a test user
@pytest.fixture
def new_user_data():
    return {
        "first_name": "Test",
        "last_name": "User",
        "email": "test.user@example.com"
    }

@pytest.fixture
def update_user_data():
    return {
        "first_name": "Updated",
        "last_name": "User",
        "email": "updated.user@example.com"
    }


def test_create_user(new_user_data):
    """Test creating a new user (POST)."""
    response = requests.post(BASE_URL + "/", json=new_user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["first_name"] == new_user_data["first_name"]
    assert data["last_name"] == new_user_data["last_name"]
    assert data["email"] == new_user_data["email"]

    global USER_ID
    USER_ID = data["id"]  # Store the user ID for subsequent tests


def test_get_user_by_id():
    """Test retrieving a user by ID (GET)."""
    if not USER_ID:
        pytest.skip("No user ID available, create user test likely failed")

    response = requests.get(f"{BASE_URL}/{USER_ID}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == USER_ID


def test_get_all_users():
    """Test retrieving a list of users (GET)."""
    response = requests.get(BASE_URL + "/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_user(update_user_data):
    """Test updating a user (PUT)."""
    if not USER_ID:
        pytest.skip("No user ID available, create user test likely failed")

    response = requests.put(f"{BASE_URL}/{USER_ID}", json=update_user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == USER_ID
    assert data["first_name"] == update_user_data["first_name"]
    assert data["last_name"] == update_user_data["last_name"]
    assert data["email"] == update_user_data["email"]

def test_create_duplicate_user(new_user_data):
    """Test creating a user with duplicate email."""
    response = requests.post(BASE_URL + "/", json=new_user_data)
    assert response.status_code == 400
    data = response.json()
    assert data["error"] == "Email already registered"
