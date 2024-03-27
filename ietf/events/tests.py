from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from wagtail.models import Page, Site


from ..home.factories import HomePageFactory
from ..home.models import HomePage
from .factories import EventListingPageFactory, EventPageFactory
from .models import EventListingPage, EventPage


class EventPageTests(TestCase):
    def setUp(self):
        root = Page.get_first_root_node()
        self.home: HomePage = HomePageFactory(parent=root)  # type: ignore

        site = Site.objects.get()
        site.root_page = self.home
        site.save(update_fields=["root_page"])

        self.event_listing: EventListingPage = EventListingPageFactory(
            parent=self.home,
        )  # type: ignore
        self.event_page: EventPage = EventPageFactory(
            parent=self.event_listing,
            end_date=timezone.now() + timedelta(days=1),
        )  # type: ignore

    def test_event_listing(self):
        response = self.client.get(path=self.event_listing.url)
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()

        self.assertIn(self.event_page.title, html)
        self.assertIn(f'href="{self.event_page.url}"', html)

    def test_event_page(self):
        response = self.client.get(path=self.event_page.url)
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()

        self.assertIn(self.event_page.title, html)
        self.assertIn(self.event_page.introduction, html)
        self.assertIn(f'href="{self.event_listing.url}"', html)

    def test_home_page(self):
        response = self.client.get(path=self.home.url)
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()

        self.assertIn(f'href="{self.event_page.url}"', html)
        self.assertIn(self.event_page.title, html)
