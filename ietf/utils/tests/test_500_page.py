from unittest.mock import Mock
from django.test import Client
import pytest

pytestmark = pytest.mark.django_db


def test_500_page(client: Client, monkeypatch: pytest.MonkeyPatch, settings, home):
    settings.DEBUG = False
    monkeypatch.setattr(
        "ietf.home.models.HomePage.serve", Mock(side_effect=RuntimeError)
    )
    client.raise_request_exception = False
    response = client.get("/")
    assert response.status_code == 500
    expect = 'If the matter is urgent, please email <a href="mailto:support@ietf.org">'
    assert expect in response.content.decode()
