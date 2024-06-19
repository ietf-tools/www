import pytest
from django.test import Client

from ietf.home.models import HomePage

from .factories import GlossaryPageFactory
from .models import GlossaryPage

pytestmark = pytest.mark.django_db


class TestGlossaryPage:
    @pytest.fixture(autouse=True)
    def set_up(self, home: HomePage, client: Client):
        self.home = home
        self.client = client
        self.glossary_page: GlossaryPage = GlossaryPageFactory(
            parent=self.home,
        )  # type: ignore

    def test_glossary_page(self):
        response = self.client.get(path=self.glossary_page.url)
        assert response.status_code == 200
        html = response.content.decode()

        assert self.glossary_page.title in html
        assert self.glossary_page.introduction in html
