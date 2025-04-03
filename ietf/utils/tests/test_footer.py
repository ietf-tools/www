import pytest
from bs4 import BeautifulSoup
from django.test import Client, RequestFactory

from ietf.home.models import HomePage
from ietf.standard.factories import StandardIndexPageFactory, StandardPageFactory
from ietf.standard.models import StandardIndexPage, StandardPage
from ietf.utils.models import FooterColumn

pytestmark = pytest.mark.django_db


class TestFooterColumns:
    @pytest.fixture(autouse=True)
    def set_up(self, home: HomePage, client: Client):
        self.home = home
        self.client = client

        self.standard_index: StandardIndexPage = StandardIndexPageFactory(
            parent=self.home,
        )  # type: ignore

        self.standard_page: StandardPage = StandardPageFactory(
            parent=self.standard_index,
            show_in_menus=True,
        )  # type: ignore

    def test_links(self):
        FooterColumn.objects.create(
            title="Column Title",
            links=[
                {
                    "type": "link",
                    "value": {
                        "page": self.standard_index.pk,
                    },
                },
                {
                    "type": "link",
                    "value": {
                        "page": self.standard_page.pk,
                        "title": "My Page Title",
                    },
                },
                {
                    "type": "link",
                    "value": {
                        "external_url": "http://example.com",
                    },
                },
                {
                    "type": "link",
                    "value": {
                        "external_url": "http://example.com",
                        "title": "My External Link Title",
                    },
                },
            ],
            sort_order=1,
        )

        response = self.client.get("/")
        assert response.status_code == 200
        html = response.content.decode()
        soup = BeautifulSoup(html, "html.parser")

        # Select the single footer column.
        [section] = soup.select("footer section")

        # Select the column's heading.
        [h4] = section.select("h4")
        assert h4.get_text().strip() == "Column Title"

        # Select the links. They should match what we specified in the `links`
        # field.
        [link1, link2, link3, link4] = section.select("ul li a")
        assert link1.get_text().strip() == self.standard_index.title
        assert link1.attrs["href"] == self.standard_index.url
        assert link2.get_text().strip() == "My Page Title"
        assert link2.attrs["href"] == self.standard_page.url
        assert link3.get_text().strip() == "http://example.com"
        assert link3.attrs["href"] == "http://example.com"
        assert link4.get_text().strip() == "My External Link Title"
        assert link4.attrs["href"] == "http://example.com"

    def test_order_in_preview(self):
        item1 = FooterColumn.objects.create(title="One", sort_order=10)
        FooterColumn.objects.create(title="Two", sort_order=20)

        item1.sort_order = 30
        context = item1.get_preview_context(RequestFactory().get("/"), "")
        assert [i.title for i in context["FOOTER"]] == ["Two", "One"]

    def test_order_in_preview_new_object(self):
        FooterColumn.objects.create(title="One", sort_order=10)
        item2 = FooterColumn(title="Two", sort_order=5)

        context = item2.get_preview_context(RequestFactory().get("/"), "")
        assert [i.title for i in context["FOOTER"]] == ["Two", "One"]
