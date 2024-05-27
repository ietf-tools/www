import pytest
from django.test import Client
from django.urls import reverse
from wagtail.models import Page

from ietf.home.models import HomePage
from ietf.standard.factories import StandardPageFactory
from ietf.standard.models import StandardPage

pytestmark = pytest.mark.django_db


class TestSearch:
    @pytest.fixture(autouse=True)
    def set_up(self, home: HomePage, client: Client):
        self.home = home
        self.client = client

        self.standard_page: StandardPage = StandardPageFactory(
            parent=self.home,
            introduction="Some random introduction text",
        )  # type: ignore

    def test_search(self):
        query = "random"
        resp = self.client.get(f"{reverse('search')}?query={query}")
        assert resp.status_code == 200

        assert resp.context["search_query"] == query
        assert list(resp.context["search_results"]) == \
            [Page.objects.get(pk=self.standard_page.pk)]

    def test_empty_query(self):
        resp = self.client.get(f"{reverse('search')}?query=")
        assert resp.status_code == 200

    def test_empty_page(self):
        query = "random"
        resp = self.client.get(f"{reverse('search')}?query={query}&page=100")
        assert resp.status_code == 200
        assert list(resp.context["search_results"]) == \
            [Page.objects.get(pk=self.standard_page.pk)]

    def test_non_integer_page(self):
        query = "random"
        resp = self.client.get(f"{reverse('search')}?query={query}&page=foo")
        assert resp.status_code == 200
        assert list(resp.context["search_results"]) == \
            [Page.objects.get(pk=self.standard_page.pk)]
