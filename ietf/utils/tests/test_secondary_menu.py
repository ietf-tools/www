from django.test import Client
import pytest
from wagtail.test.utils import WagtailTestUtils

from ietf.events.factories import EventListingPageFactory, EventPageFactory
from ietf.home.models import HomePage
from ietf.utils.models import SecondaryMenuItem

pytestmark = pytest.mark.django_db


class TestMenu(WagtailTestUtils):
    @pytest.fixture(autouse=True)
    def set_up(self, home: HomePage):
        self.home = home
        self.eventlisting = EventListingPageFactory(
            parent=home,
        )
        self.eventpage = EventPageFactory(
            parent=self.eventlisting,
        )

    def _build_menu(self):
        SecondaryMenuItem.objects.create(page=self.eventlisting, text="Menu One", sort_order=0)
        SecondaryMenuItem.objects.create(page=self.eventpage, text="Menu Two", sort_order=1)

    def test_admin_menu_item_index(self, admin_client):
        response = admin_client.get("/admin/utils/secondarymenuitem/")
        assert response.status_code == 200

    def test_menu_context_loads(self, client: Client):
        self._build_menu()
        menu_items = SecondaryMenuItem.objects.order_by("sort_order").all()
        response = client.get("/")
        assert response.status_code == 200
        secondary_menu = response.context["SECONDARY_MENU"]()
        assert len(secondary_menu) == 2
        assert menu_items[0] == secondary_menu[0]
        assert menu_items[1] == secondary_menu[1]

    def test_menu_in_template(self, client: Client):
        self._build_menu()
        response = client.get("/")
        html = response.content.decode()
        assert "Menu Two" in html
        assert "Menu One" in html
