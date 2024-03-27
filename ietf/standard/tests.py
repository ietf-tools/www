from django.test import TestCase
from wagtail.models import Page, Site

from ..home.factories import HomePageFactory
from ..home.models import HomePage
from .factories import StandardIndexPageFactory, StandardPageFactory
from .models import StandardIndexPage, StandardPage


class StandardPageTests(TestCase):
    def setUp(self):
        root = Page.get_first_root_node()
        self.home: HomePage = HomePageFactory(parent=root)  # type: ignore

        site = Site.objects.get()
        site.root_page = self.home
        site.save(update_fields=["root_page"])

        self.standard_index: StandardIndexPage = StandardIndexPageFactory(
            parent=self.home,
        )  # type: ignore

        self.standard_page: StandardPage = StandardPageFactory(
            parent=self.standard_index,
        )  # type: ignore

    def test_index_page(self):
        response = self.client.get(path=self.standard_index.url)
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()

        self.assertIn(self.standard_page.title, html)
        self.assertIn(f'href="{self.standard_page.url}"', html)

    def test_standard_page(self):
        response = self.client.get(path=self.standard_page.url)
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()

        self.assertIn(self.standard_page.title, html)
        self.assertIn(self.standard_page.introduction, html)
        self.assertIn(f'href="{self.standard_index.url}"', html)
