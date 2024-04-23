from unittest.mock import MagicMock, patch
from datetime import date, timedelta
import datetime
import pytest

from src.database.models import User
from src.services.auth import auth_service
from tests.test_route_one_contact import token


def test_read_contacts(client, token):
    with patch.object(auth_service, 'cache') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/contacts",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert isinstance(data, list)
        # assert data[0]["name"] == "test_tag"
        assert "id" in data[0]