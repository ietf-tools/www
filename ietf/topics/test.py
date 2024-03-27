from django.test import TestCase
from wagtail.models import Page, Site

from ..home.factories import HomePageFactory
from ..home.models import HomePage
from .factories import PrimaryTopicPageFactory, TopicIndexPageFactory
from .models import PrimaryTopicPage, TopicIndexPage


class TopicPageTests(TestCase):
    def setUp(self):
        root = Page.get_first_root_node()
        self.home: HomePage = HomePageFactory(parent=root)  # type: ignore

        site = Site.objects.get()
        site.root_page = self.home
        site.save(update_fields=["root_page"])

        self.topic_index: TopicIndexPage = TopicIndexPageFactory(
            parent=self.home,
        )  # type: ignore

        self.topic_page: PrimaryTopicPage = PrimaryTopicPageFactory(
            parent=self.topic_index,
        )  # type: ignore

    def test_index_page(self):
        response = self.client.get(path=self.topic_index.url)
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()

        self.assertIn(self.topic_page.title, html)
        self.assertIn(f'href="{self.topic_page.url}"', html)

    def test_topic_page(self):
        response = self.client.get(path=self.topic_page.url)
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()

        self.assertIn(self.topic_page.title, html)
        self.assertIn(self.topic_page.introduction, html)
        self.assertIn(f'href="{self.topic_index.url}"', html)
