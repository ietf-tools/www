from datetime import timedelta

import pytest
from django.test import Client
from django.utils import timezone

from ietf.home.models import HomePage
from .factories import EventListingPageFactory, EventPageFactory
from .models import EventListingPage, EventPage

pytestmark = pytest.mark.django_db


class TestEventPage:
    @pytest.fixture(autouse=True)
    def set_up(self, home: HomePage, client: Client):
        self.home = home
        self.client = client

        self.event_listing: EventListingPage = EventListingPageFactory(
            parent=self.home,
        )  # type: ignore
        self.event_page: EventPage = EventPageFactory(
            parent=self.event_listing,
            end_date=timezone.now() + timedelta(days=1),
            body__0__heading="Heading in body Streamfield",
        )  # type: ignore

    def test_event_listing(self):
        response = self.client.get(path=self.event_listing.url)
        assert response.status_code == 200
        html = response.content.decode()

        assert self.event_page.title in html
        assert f'href="{self.event_page.url}"' in html

    def test_event_page(self):
        response = self.client.get(path=self.event_page.url)
        assert response.status_code == 200
        html = response.content.decode()

        assert self.event_page.title in html
        assert self.event_page.body[0].value in html
        assert self.event_page.introduction in html
        assert f'href="{self.event_listing.url}"' in html

    def test_home_page(self):
        response = self.client.get(path=self.home.url)
        assert response.status_code == 200
        html = response.content.decode()

        assert f'href="{self.event_page.url}"' in html
        assert self.event_page.title in html
