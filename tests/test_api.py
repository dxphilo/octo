from fastapi.testclient import TestClient
from datetime import datetime

from main import app

client = TestClient(app)

sign_up_info = {
        "fullname":"John Philip",
        "email":"john@gmail.com",
        "password":"OkwonkowoNaKitambiUtawezana",
        }


def test_health_check():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"Message": "Server is up and running"}

def test_user_creation():
    response = client.post('/signup/',json=sign_up_info)
    assert response.status_code == 201

