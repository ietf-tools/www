from bs4 import BeautifulSoup
from django.test import Client
import pytest

from ietf.home.models import IABHomePage
from ietf.standard.factories import IABStandardPageFactory

pytestmark = pytest.mark.django_db


class TestIABHome:
    @pytest.fixture(autouse=True)
    def set_up(self, iab_home: IABHomePage, client: Client):
        self.home = iab_home
        self.client = client

    def test_pages_in_menu(self):
        page1 = IABStandardPageFactory(parent=self.home, show_in_menus=True)
        page1a = IABStandardPageFactory(parent=page1, show_in_menus=True)
        page1b = IABStandardPageFactory(parent=page1, show_in_menus=True)
        page2 = IABStandardPageFactory(parent=self.home, show_in_menus=True)
        page2a = IABStandardPageFactory(parent=page2, show_in_menus=True)
        page2b = IABStandardPageFactory(parent=page2, show_in_menus=True)

        response = self.client.get(path=self.home.url)
        assert response.status_code == 200
        html = response.content.decode()
        soup = BeautifulSoup(html, "html.parser")

        def get_nav_item(item):
            [main_link] = item.select("a.nav-link")
            child_links = item.select("ul.dropdown-menu > li > a")
            return (
                main_link.attrs["href"],
                [link.attrs["href"] for link in child_links],
            )

        menu = [get_nav_item(item) for item in soup.select(".navbar-nav > li")]
        assert menu == [
            (page1.url, [page1a.url, page1b.url]),
            (page2.url, [page2a.url, page2b.url]),
            ('/search', []),
        ]
