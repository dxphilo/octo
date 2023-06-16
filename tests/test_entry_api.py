import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@pytest.fixture
def authorization_headers():
    return {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiVGVzdCBDaGl6aSIsInVzZXJfZW1haWwiOiJjaGl6aUBnbWFpbC5jb20iLCJyb2xlIjoiYWRtaW4iLCJleHBpcmVzIjoxNjg2OTc0NzMxLjY3MjM0NTJ9.wA3hQOFR3xgLcBjPXnJQqp-coz_z7UOrciA_hncW_ks"
    }

@pytest.fixture
def sample_entry_payload():
    return {
        "text": "Kuku Choma"
    }


@pytest.fixture
def sample_update_payload():
    return {
        "fullname": "Pro Admin",
        "email": "admin50@gmail.com",
        "password": "this is an updated field",
        "role": "admin"
    }


# Test should fail is no Auth token is specified/payload is provided
def test_entry_creation(sample_entry_payload, authorization_headers):
    response = client.post('/user/entries/', headers = authorization_headers,json=sample_entry_payload)
    assert response.status_code == 201
    entry = response.json()
    assert isinstance(entry,dict)
    assert all(key in entry for key in ["id", "user", "number_of_calories", "is_under_calories", "date", "time"])
    assert isinstance(entry['id'],int)
    assert isinstance(entry['number_of_calories'],str)
    assert isinstance(entry['is_under_calories'],bool)
    assert isinstance(entry['date'],str)
    assert isinstance(entry['time'],str)
    assert entry["text"] == sample_entry_payload["text"]
    assert "user" in entry


