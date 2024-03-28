from bs4 import BeautifulSoup
import pytest
from django.test import Client, RequestFactory
from wagtail.models import Page, Site

from ietf.home.factories import HomePageFactory
from ietf.home.models import HomePage
from ietf.standard.factories import StandardIndexPageFactory, StandardPageFactory
from ietf.standard.models import StandardIndexPage, StandardPage
from ietf.utils.models import MainMenuItem

pytestmark = pytest.mark.django_db


class TestMegaMenu:
    @pytest.fixture(autouse=True)
    def set_up(self, client: Client):
        self.client = client

        root = Page.get_first_root_node()
        self.home: HomePage = HomePageFactory(parent=root)  # type: ignore

        site = Site.objects.get()
        site.root_page = self.home
        site.save(update_fields=["root_page"])

        self.standard_index: StandardIndexPage = StandardIndexPageFactory(
            parent=self.home,
        )  # type: ignore

        self.standard_page: StandardPage = StandardPageFactory(
            parent=self.standard_index,
            show_in_menus=True,
        )  # type: ignore

    def test_primary_section(self):
        MainMenuItem.objects.create(page=self.standard_index, sort_order=1)

        response = self.client.get("/")
        assert response.status_code == 200
        html = response.content.decode()
        soup = BeautifulSoup(html, "html.parser")

        [button] = soup.select(".megamenu__toggle")
        assert button.get_text().strip() == self.standard_index.title

        [menu] = soup.select(".megamenu__menu")
        [primary_heading] = menu.select("h5")
        assert primary_heading.get_text().strip() == self.standard_index.title
        assert primary_heading.select("a")[0].attrs["href"] == self.standard_index.url

        primary_linklist = menu.select("ul.megamenu__linklist")[0]
        [page_link] = primary_linklist.select("li a")
        assert page_link.get_text().strip() == self.standard_page.title
        assert page_link.attrs["href"] == self.standard_page.url

    def test_secondary_section(self):
        MainMenuItem.objects.create(
            page=self.standard_index,
            sort_order=1,
            secondary_sections=[
                {
                    "type": "section",
                    "value": {
                        "title": "Secondary Links",
                        "links": [
                            {"page": self.standard_index.pk},
                            {"page": self.standard_page.pk, "title": "Alternate Title"},
                            {"external_url": "http://example.com"},
                            {"external_url": "http://example.com", "title": "External"},
                        ],
                    },
                },
            ],
        )

        response = self.client.get("/")
        assert response.status_code == 200
        html = response.content.decode()
        soup = BeautifulSoup(html, "html.parser")

        [menu] = soup.select(".megamenu__menu")
        [secondary_heading] = menu.select("h6")
        assert secondary_heading.get_text() == "Secondary Links"

        secondary_linklist = menu.select("ul.megamenu__linklist")[1]
        [link1, link2, link3, link4] = secondary_linklist.select("li a")
        assert link1.get_text().strip() == self.standard_index.title
        assert link1.attrs["href"] == self.standard_index.url
        assert link2.get_text().strip() == "Alternate Title"
        assert link2.attrs["href"] == self.standard_page.url
        assert link3.get_text().strip() == "http://example.com"
        assert link3.attrs["href"] == "http://example.com"
        assert link4.get_text().strip() == "External"
        assert link4.attrs["href"] == "http://example.com"

    def test_order_in_preview(self):
        item1 = MainMenuItem.objects.create(page=self.standard_index, sort_order=10)
        item2 = MainMenuItem.objects.create(page=self.standard_page, sort_order=20)

        item1.sort_order = 30
        context = item1.get_preview_context(RequestFactory().get("/"), "")
        assert [i["url"] for i in context["MENU"]] == [
            self.standard_page.url,
            self.standard_index.url,
        ]

    def test_order_in_preview_new_object(self):
        item1 = MainMenuItem.objects.create(page=self.standard_index, sort_order=10)
        item2 = MainMenuItem(page=self.standard_page, sort_order=5)

        context = item2.get_preview_context(RequestFactory().get("/"), "")
        assert [i["url"] for i in context["MENU"]] == [
            self.standard_page.url,
            self.standard_index.url,
        ]
