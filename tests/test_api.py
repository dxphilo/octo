from fastapi.testclient import TestClient
from datetime import datetime

from main import app

client = TestClient(app)

sign_up_info = {
        "fullname":"John Philip",
        "email":"johnn@gmail.com",
        "password":"OkwonkowoNaKitambiUtawezana",
        "role":"admin"
        }


def test_health_check():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == {"status": "ok 👍 "}

def test_user_creation():
    response = client.post('/signup/',json=sign_up_info)
    assert response.status_code == 201

