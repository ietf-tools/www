from django.test import TestCase
from wagtail.models import Page, Site

from ietf.standard.factories import StandardPageFactory
from ietf.standard.models import StandardPage

from .factories import HomePageFactory
from .models import HomePage


class HomeTests(TestCase):
    def setUp(self):
        root = Page.get_first_root_node()
        self.home: HomePage = HomePageFactory(parent=root)  # type: ignore
        self.assertEqual(HomePage.objects.count(), 1)

        site = Site.objects.get()
        site.root_page = self.home
        site.save(update_fields=["root_page"])

    def test_homepage(self):
        response = self.client.get(path=self.home.url)
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()

        self.assertIn(self.home.title, html)
        self.assertIn(self.home.heading, html)
        self.assertIn(self.home.introduction, html)

    def test_button(self):
        page: StandardPage = StandardPageFactory(
            parent=self.home,
        )  # type: ignore
        self.home.button_text = "Homepage button text"
        self.home.button_link = page
        self.home.save(update_fields=["button_text", "button_link"])

        response = self.client.get(path=self.home.url)
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()

        self.assertIn(self.home.button_text, html)
        self.assertIn(f'href="{page.url}"', html)
