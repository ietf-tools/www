from django.test import TestCase
from django.utils import timezone
from wagtail.models import Page, Site

from ..home.factories import HomePageFactory
from ..home.models import HomePage
from .factories import IESGStatementIndexPageFactory, IESGStatementPageFactory
from .models import IESGStatementIndexPage, IESGStatementPage


class IESGStatementPageTests(TestCase):
    def setUp(self):
        root = Page.get_first_root_node()
        self.home: HomePage = HomePageFactory(parent=root)  # type: ignore

        site = Site.objects.get()
        site.root_page = self.home
        site.save(update_fields=["root_page"])

        self.index: IESGStatementIndexPage = IESGStatementIndexPageFactory(
            parent=self.home,
        )  # type: ignore

        self.statement: IESGStatementPage = IESGStatementPageFactory(
            parent=self.index,
            date_published=timezone.now(),
        )  # type: ignore

    def test_index_page(self):
        response = self.client.get(path=self.index.url)
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()

        self.assertIn(self.statement.title, html)
        self.assertIn(f'href="{self.statement.url}"', html)

    def test_statement_page(self):
        response = self.client.get(path=self.statement.url)
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()

        self.assertIn(self.statement.title, html)
        self.assertIn(self.statement.introduction, html)
        self.assertIn(f'href="{self.index.url}"', html)
