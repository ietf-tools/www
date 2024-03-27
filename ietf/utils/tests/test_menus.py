from django.test import TestCase
from wagtail.models import Page, Site
from wagtail.test.utils import WagtailTestUtils

from ietf.events.models import EventListingPage, EventPage
from ietf.home.models import HomePage
from ietf.utils.models import SecondaryMenuItem


class MenuTests(TestCase, WagtailTestUtils):
    def setUp(self):
        super().setUp()
        self._setup_pages()
        self.login()

    def _setup_pages(self):
        root = Page.get_first_root_node()

        home = HomePage(
            slug="homepageslug",
            title="home page title",
            heading="home page heading",
            introduction="home page introduction",
        )

        root.add_child(instance=home)

        Site.objects.all().delete()

        Site.objects.create(
            hostname="localhost",
            root_page=home,
            is_default_site=True,
            site_name="testingsitename",
        )

        self.eventlisting = EventListingPage(
            slug="eventlisting",
            title="event listing page title",
            introduction="event listing page introduction",
        )
        home.add_child(instance=self.eventlisting)

        self.eventpage = EventPage(
            slug="event",
            title="event title",
            introduction="event introduction",
        )
        self.eventlisting.add_child(instance=self.eventpage)

    def _build_menu(self):
        SecondaryMenuItem.objects.create(page=self.eventlisting, text="Menu One", sort_order=0)
        SecondaryMenuItem.objects.create(page=self.eventpage, text="Menu Two", sort_order=1)

    def test_admin_menu_item_index(self):
        response = self.client.get("/admin/utils/secondarymenuitem/")
        self.assertEqual(response.status_code, 200)

    def test_menu_context_loads(self):
        self._build_menu()
        menu_items = SecondaryMenuItem.objects.order_by("sort_order").all()
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        secondary_menu = response.context["SECONDARY_MENU"]()
        self.assertEqual(len(secondary_menu), 2)
        self.assertEqual(menu_items[0], secondary_menu[0])
        self.assertEqual(menu_items[1], secondary_menu[1])

    def test_menu_in_template(self):
        self._build_menu()
        menu_items = SecondaryMenuItem.objects.order_by("sort_order").all()
        response = self.client.get("/")
        self.assertContains(
            response, "Menu Two".format(menu_items[1].page.url), count=1
        )
        self.assertContains(
            response, "Menu One".format(menu_items[0].page.url), count=1
        )
