from django.test import TestCase
from wagtail.models import Page, Site

from ietf.home.factories import HomePageFactory

from ..home.models import HomePage
from .factories import GlossaryPageFactory
from .models import GlossaryPage


class GlossaryPageTests(TestCase):
    def setUp(self):
        root = Page.get_first_root_node()
        self.home: HomePage = HomePageFactory(parent=root)  # type: ignore
        self.assertEqual(HomePage.objects.count(), 1)

        site = Site.objects.get()
        site.root_page = self.home
        site.save(update_fields=["root_page"])

        self.glossary_page: GlossaryPage = GlossaryPageFactory(
            parent=self.home,
        )  # type: ignore

    def test_glossary_page(self):
        response = self.client.get(path=self.glossary_page.url)
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()

        self.assertIn(self.glossary_page.title, html)
        self.assertIn(self.glossary_page.introduction, html)
