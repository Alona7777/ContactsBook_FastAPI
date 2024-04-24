from unittest.mock import MagicMock, patch
from datetime import date, timedelta
import datetime
import pytest

from src.database.models import User
from src.services.auth import auth_service

test_json = {
    "first_name": "string",
    "last_name": "string",
    "email": "user@example.com",
    "phone": "4242474890",
    "birth_date": "2024-11-23",
    "info": "string",
}
test_json_1 = {
    "first_name": "test",
    "last_name": "test",
    "email": "user@example.com",
    "phone": "4242574890",
    "birth_date": "2010-10-23",
    "info": "string",
}

@pytest.fixture()
def token(client, user, session, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    client.post("/api/auth/signup", json=user)
    current_user: User = (
        session.query(User).filter(User.email == user.get("email")).first()
    )
    current_user.confirmed = True
    session.commit()
    response = client.post(
        "/api/auth/login",
        data={"username": user.get("email"), "password": user.get("password")},
    )
    data = response.json()
    return data["access_token"]


def test_create_contact(client, token):
    with patch.object(auth_service, "cache") as r_mock:
        r_mock.get.return_value = None
        response = client.post(
            "/api/contact",
            json=test_json,
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 201, response.text
        data = response.json()
        assert data["email"] == test_json.get("email")
        assert "id" in data


def test_read_contact(client, token):
    with patch.object(auth_service, "cache") as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/contact/1", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["email"] == test_json.get("email")
        assert "id" in data


def test_read_contact_by_email(client, token):
    with patch.object(auth_service, "cache") as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/contact/search/user@example.com",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["email"] == test_json.get("email")
        assert "id" in data


def test_get_contact_not_found(client, token):
    with patch.object(auth_service, "cache") as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/contact/2", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Contact not found"


def test_read_contacts(client, token):  # to move to the test_route_contacts.py
    with patch.object(auth_service, "cache") as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/contacts", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert isinstance(data, list)
        assert data[0]["email"] == test_json.get("email")
        assert "id" in data[0]


def test_update_contact(client, token):
    with patch.object(auth_service, "cache") as r_mock:
        r_mock.get.return_value = None
        response = client.put(
            "/api/contact/1",
            json=test_json_1,
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200, response.text
        data = response.json()
        # assert data["email"] == test_json.get("email")
        # assert "id" in data


def test_update_contact_not_found(client, token):
    with patch.object(auth_service, "cache") as r_mock:
        r_mock.get.return_value = None
        response = client.put(
            "/api/contact/2",
            json=test_json,
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Contact not found"


# def test_delete_tag(client, token):
#     with patch.object(auth_service, 'r') as r_mock:
#         r_mock.get.return_value = None
#         response = client.delete(
#             "/api/tags/1",
#             headers={"Authorization": f"Bearer {token}"}
#         )
#         assert response.status_code == 200, response.text
#         data = response.json()
#         assert data["name"] == "new_test_tag"
#         assert "id" in data


# def test_repeat_delete_tag(client, token):
#     with patch.object(auth_service, 'r') as r_mock:
#         r_mock.get.return_value = None
#         response = client.delete(
#             "/api/tags/1",
#             headers={"Authorization": f"Bearer {token}"}
#         )
#         assert response.status_code == 404, response.text
#         data = response.json()
#         assert data["detail"] == "Tag not found"
