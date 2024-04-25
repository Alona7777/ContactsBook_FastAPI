from unittest.mock import MagicMock, Mock

from src.database.models import User
from src.conf import messages


def test_create_user(client, user, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    response = client.post(
        "/api/auth/signup",
        json=user,
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["username"] == user.get("username")
    assert data["email"] == user.get("email")
    assert "password" not in data
    assert "avatar" in data


def test_repeat_create_user(client, user, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    response = client.post(
        "/api/auth/signup",
        json=user,
    )
    assert response.status_code == 409, response.text
    data = response.json()
    assert data["detail"] == messages.ACCOUNT_EXIST


def test_login_user_not_confirmed(client, user):
    response = client.post(
        "/api/auth/login",
        data={"username": user.get("email"), "password": user.get("password")},
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == messages.EMAIL_NOT_CONFIRMED


def test_login_user(client, session, user):
    current_user: User = (
        session.query(User).filter(User.email == user.get("email")).first()
    )
    current_user.confirmed = True
    session.commit()
    response = client.post(
        "/api/auth/login",
        data={"username": user.get("email"), "password": user.get("password")},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert "token_type" in data


def test_login_wrong_password(client, user):
    response = client.post(
        "/api/auth/login",
        data={"username": user.get("email"), "password": "password"},
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == messages.WRONG_PASSWORD


def test_login_wrong_email(client, user):
    response = client.post(
        "/api/auth/login",
        data={"username": "email", "password": user.get("password")},
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == messages.WRONG_EMAIL

def test_validation_error_login(client, user):
    response = client.post("api/auth/login",
                           data={"password": user.get("password")})
    assert response.status_code == 422, response.text
    data = response.json()
    assert "detail" in data  
