from datetime import timedelta
from bs4 import BeautifulSoup
from django.test import Client
from django.utils import timezone

import pytest

from ietf.home.models import IABHomePage
from .factories import IABAnnouncementIndexPageFactory, IABAnnouncementPageFactory
from .models import IABAnnouncementIndexPage, IABAnnouncementPage

pytestmark = pytest.mark.django_db


class TestIABAnnouncement:
    @pytest.fixture(autouse=True)
    def set_up(self, iab_home: IABHomePage, client: Client):
        self.home = iab_home
        self.client = client

        self.index: IABAnnouncementIndexPage = IABAnnouncementIndexPageFactory(
            parent=self.home,
        )  # type: ignore

        now = timezone.now()

        self.announcement_1: IABAnnouncementPage = IABAnnouncementPageFactory(
            parent=self.index,
            date=now - timedelta(days=10),
        )  # type: ignore

        self.announcement_2: IABAnnouncementPage = IABAnnouncementPageFactory(
            parent=self.index,
            date=now - timedelta(days=8),
        )  # type: ignore

        self.announcement_3: IABAnnouncementPage = IABAnnouncementPageFactory(
            parent=self.index,
            date=now - timedelta(days=4),
        )  # type: ignore

        self.announcement_4: IABAnnouncementPage = IABAnnouncementPageFactory(
            parent=self.index,
            date=now,
        )  # type: ignore

    def test_announcement_page(self):
        response = self.client.get(self.announcement_3.url)
        assert response.status_code == 200
        html = response.content.decode()

        assert self.announcement_3.title in html
        assert self.announcement_3.introduction in html

    def test_homepage(self):
        response = self.client.get(self.home.url)
        assert response.status_code == 200
        html = response.content.decode()

        assert f'href="{self.announcement_3.url}"' in html
        assert self.announcement_3.title in html
        assert f'href="{self.announcement_4.url}"' in html
        assert self.announcement_4.title in html

    def test_index_page(self):
        response = self.client.get(self.index.url)
        assert response.status_code == 200
        html = response.content.decode()
        soup = BeautifulSoup(html, "html.parser")
        links = [a.get_text().strip() for a in soup.select("#content .container h2 a")]
        assert links == [
            self.announcement_4.title,
            self.announcement_3.title,
            self.announcement_2.title,
            self.announcement_1.title,
        ]
