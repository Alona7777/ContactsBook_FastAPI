from unittest.mock import MagicMock, patch
from datetime import date, timedelta
import datetime
import pytest

from src.database.models import User
from src.conf import messages
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
    "first_name": "string",
    "last_name": "string",
    "email": "user@example.com",
    "phone": "4242474890",
    "birth_date":  datetime.date(2024, 4, 23).isoformat(),  
    "info": "string",
}


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
        assert data["detail"] == messages.NOT_CONTACT


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


# def test_update_contact(client, token):
#     with patch.object(auth_service, "cache") as r_mock:
#         r_mock.get.return_value = None
#         response = client.put(
#             "/api/contact/1",
#             json=test_json_1,
#             headers={"Authorization": f"Bearer {token}"},
#         )
#         assert response.status_code == 200, response.text
#         data = response.json()
#         # assert data["email"] == test_json.get("email")
#         # assert "id" in data


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
        assert data["detail"] == messages.NOT_CONTACT

def test_update_name(client, token):
    with patch.object(auth_service, "cache") as r_mock:
        r_mock.get.return_value = None
        response = client.patch(
            "/api/contact/update_name/1/test",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["email"] == test_json.get("email")
        assert data["first_name"] == "test"
        assert "id" in data


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
#         assert data["detail"] == messages.NOT_CONTACT
