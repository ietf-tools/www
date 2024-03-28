from django.test import TestCase
from django.urls import reverse
from wagtail.models import Page, Site

from ..home.factories import HomePageFactory
from ..standard.factories import StandardPageFactory
from ..standard.models import StandardPage


class SearchTests(TestCase):
    def setUp(self):
        root = Page.get_first_root_node()
        self.home: HomePage = HomePageFactory(parent=root)  # type: ignore

        site = Site.objects.get()
        site.root_page = self.home
        site.save(update_fields=["root_page"])

        self.standard_page: StandardPage = StandardPageFactory(
            parent=self.home,
            introduction="Some random introduction text",
        )  # type: ignore

    def test_search(self):
        query = "random"
        resp = self.client.get(f"{reverse('search')}?query={query}")
        self.assertEqual(resp.status_code, 200)

        self.assertEqual(resp.context["search_query"], query)
        self.assertEqual(
            list(resp.context["search_results"]),
            [Page.objects.get(pk=self.standard_page.pk)],
        )

    def test_empty_query(self):
        resp = self.client.get(f"{reverse('search')}?query=")
        self.assertEqual(resp.status_code, 200)

    def test_empty_page(self):
        query = "random"
        resp = self.client.get(f"{reverse('search')}?query={query}&page=100")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            list(resp.context["search_results"]),
            [Page.objects.get(pk=self.standard_page.pk)],
        )

    def test_non_integer_page(self):
        query = "random"
        resp = self.client.get(f"{reverse('search')}?query={query}&page=foo")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            list(resp.context["search_results"]),
            [Page.objects.get(pk=self.standard_page.pk)],
        )
