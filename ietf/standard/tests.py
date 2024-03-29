from django.test import Client
import pytest

from ietf.home.models import HomePage
from .factories import StandardIndexPageFactory, StandardPageFactory
from .models import StandardIndexPage, StandardPage

pytestmark = pytest.mark.django_db


class TestStandardPage:
    @pytest.fixture(autouse=True)
    def set_up(self, home: HomePage, client: Client):
        self.home = home
        self.client = client

        self.standard_index: StandardIndexPage = StandardIndexPageFactory(
            parent=self.home,
        )  # type: ignore

        self.standard_page: StandardPage = StandardPageFactory(
            parent=self.standard_index,
        )  # type: ignore

    def test_index_page(self):
        response = self.client.get(path=self.standard_index.url)
        assert response.status_code == 200
        html = response.content.decode()

        assert self.standard_page.title in html
        assert f'href="{self.standard_page.url}"' in html

    def test_standard_page(self):
        response = self.client.get(path=self.standard_page.url)
        assert response.status_code == 200
        html = response.content.decode()

        assert self.standard_page.title in html
        assert self.standard_page.introduction in html
        assert f'href="{self.standard_index.url}"' in html
