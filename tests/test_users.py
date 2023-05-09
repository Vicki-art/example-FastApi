from app import schemas
import pytest
from app.config import settings
from jose import jwt



# def test_base_request(client): 
#     res = client.get("/")
#     assert res.json().get('message') == "Hello World"

def test_create_user(client):
    res = client.post('/users/', json = {"email": "testemail@test.com", "password": "password123"})
    new_client = schemas.CreateUserResponse(**res.json())
    assert new_client.email == "testemail@test.com"
    assert res.status_code ==201

def test_login_user(test_user, client):
    res = client.post("/login", data ={"username": test_user["email"], "password": test_user["password"]})
    logged_user = schemas.Token(**res.json())
    payload = jwt.decode(logged_user.access_token, settings.secret_key, algorithms = [settings.algorithm])
    id: str = payload.get('user_id')
    assert res.status_code == 200
    assert id == test_user['id']
    assert logged_user.token_type == "Bearer"

@pytest.mark.parametrize("email, password, status_code", [
    ("wronngemail@gmail.com", "password123", 403), ("wronngemail@gmail.com", "password123", 403), 
    ("testemail@test.com", "password1234", 403), ("wronngemail@gmail.com", "password1234", 403),
    (None, "password123", 422),("testemail@test.com", None, 422)
])

def test_login_wrong_user(test_user, client, email, password, status_code):
    res = client.post("/login", data ={"username": email, "password": password})
    assert res.status_code == status_code

