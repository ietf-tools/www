from django.test import TestCase
from wagtail.core.models import Page, Site
from wagtail.tests.utils import WagtailTestUtils

from ietf.events.models import EventListingPage, EventPage
from ietf.utils.models import MenuItem

from ..home.models import HomePage


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
            request_for_comments_section_body="rfc section body",
            working_groups_section_body="wg section body",
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
        MenuItem.objects.create(page=self.eventlisting, text="Menu One", sort_order=0)
        MenuItem.objects.create(page=self.eventpage, text="Menu Two", sort_order=1)

    def test_admin_menu_item_index(self):
        response = self.client.get("/admin/utils/menuitem/")
        self.assertEqual(response.status_code, 200)

    def test_menu_context_loads(self):
        self._build_menu()
        menu_items = MenuItem.objects.order_by("sort_order").all()
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["SECONDARY_MENU"]), 2)
        self.assertEqual(menu_items[0], response.context["SECONDARY_MENU"][0])
        self.assertEqual(menu_items[1], response.context["SECONDARY_MENU"][1])

    def test_menu_in_template(self):
        self._build_menu()
        menu_items = MenuItem.objects.order_by("sort_order").all()
        response = self.client.get("/")
        self.assertContains(
            response, "Menu Two".format(menu_items[1].page.url), count=1
        )
        self.assertContains(
            response, "Menu One".format(menu_items[0].page.url), count=1
        )
