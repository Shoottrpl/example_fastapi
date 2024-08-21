import jwt
import pytest
from app import schemas
from app.config import settings


def test_create_user(client):
    response = client.post(
        "/users", json={"email": "test6@mail.com", "password": "1337"})

    new_user = schemas.UserOut(**response.json())
    assert new_user.email == "test6@mail.com"
    assert response.status_code == 201


def test_login_user(client, test_user):
    response = client.post(
        "/login", data={"username": test_user["email"], "password": test_user["password"]})
    login_res = schemas.Token(**response.json())
    payload = jwt.decode(login_res.access_token,
                         settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert response.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ("wrongemail@mail.com", "1337", 403),
    ("test6@mail.com", "wrong", 403),
    ("wrongemail@mail.com", "wrong", 403),
    (None, "1337", 422),
    ("test6@mail.com", None, 422)
])
def test_incorrect_login(client, test_user, email, password, status_code):
    response = client.post(
        "/login", data={"username": email, "password": password})
    assert response.status_code == status_code
    # assert response.json().get("detail") == "Invalid credentials"