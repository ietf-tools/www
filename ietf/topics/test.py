import pytest
from django.test import Client

from ietf.home.models import HomePage
from .factories import PrimaryTopicPageFactory, TopicIndexPageFactory
from .models import PrimaryTopicPage, TopicIndexPage

pytestmark = pytest.mark.django_db


class TestTopicPage:
    @pytest.fixture(autouse=True)
    def set_up(self, home: HomePage, client: Client):
        self.home = home
        self.client = client

        self.topic_index: TopicIndexPage = TopicIndexPageFactory(
            parent=self.home,
        )  # type: ignore

        self.topic_page: PrimaryTopicPage = PrimaryTopicPageFactory(
            parent=self.topic_index,
        )  # type: ignore

    def test_index_page(self):
        response = self.client.get(path=self.topic_index.url)
        assert response.status_code == 200
        html = response.content.decode()

        assert self.topic_page.title in html
        assert f'href="{self.topic_page.url}"' in html

    def test_topic_page(self):
        response = self.client.get(path=self.topic_page.url)
        assert response.status_code == 200
        html = response.content.decode()

        assert self.topic_page.title in html
        assert self.topic_page.introduction in html
        assert f'href="{self.topic_index.url}"' in html
