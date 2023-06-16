import pytest
from fastapi.testclient import TestClient
from main import app
from schema.schema import DeletionSuccess

client = TestClient(app)

@pytest.fixture
def authorization_headers():
    return {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiVGVzdCBDaGl6aSIsInVzZXJfZW1haWwiOiJjaGl6aUBnbWFpbC5jb20iLCJyb2xlIjoiYWRtaW4iLCJleHBpcmVzIjoxNjg2OTYyNTc2LjMxMDkwNjJ9.fn9W1XyNVJXcqDpjcvdBbeACp_c_wnKVqz8mUmLXEMc"
    }


@pytest.fixture
def sign_up_info():
    return {
        "fullname": "Test Chizi",
        "email": "tetchizi@gmail.com",
        "password": "ChiziKarogwaTena",
        "role": "admin"
    }


@pytest.fixture
def update_user_info():
    return {
        "fullname": "Test Chizi Update",
        "email": "testchizi@gmail.com",
        "password": "ChiziKarogwaTenaUpdate",
        "role": "admin"
    }


def test_health_check():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == {"status": "ok 👍 "}

# this test will fail is user with the same email as in the test file is already registered
def test_user_creation(sign_up_info):
    response = client.post('/signup/', json=sign_up_info)
    assert response.status_code == 201


def test_user_login():
    response = client.post('/login/', json={"email": "chizi@gmail.com", "password": "ChiziKarogwaTena"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["access_token"] != ""


def test_get_users(authorization_headers):
    response = client.get('/users/', headers=authorization_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    for element in response.json():
        assert isinstance(element, dict)
        assert all(key in element for key in ["id", "fullname", "email", "role", "date", "time"])


# this test will fail is the user with the id is not found in the databse
def test_update_users(authorization_headers, update_user_info):
    user_id = 9
    response = client.put(f'/users/{user_id}', headers=authorization_headers, json=update_user_info)
    assert response.status_code == 200

    expected_elements = {
        "id": user_id,
        **update_user_info
        }

    response_json = response.json()
    assert all(key in response_json for key in expected_elements)

    for key, value in expected_elements.items():
        assert response_json[key] == value


# this test will fail is the user with the id is not found in the database
def test_delete_user(authorization_headers):
    user_id = 10
    response = client.delete(f'/users/{user_id}', headers=authorization_headers)
    assert response.status_code == 200
    assert response.json() == DeletionSuccess
