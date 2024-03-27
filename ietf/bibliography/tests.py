from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
import pytest
from django.test import TestCase
from wagtail.models import Page, Site

from ietf.bibliography.models import BibliographyItem
from ietf.snippets.models import RFC

from ..home.factories import HomePageFactory
from ..home.models import HomePage
from ..standard.factories import StandardIndexPageFactory, StandardPageFactory
from ..standard.models import StandardIndexPage, StandardPage

pytestmark = pytest.mark.django_db


class TestBibliography:
    @pytest.fixture(autouse=True)
    def set_up(self):
        root = Page.get_first_root_node()
        self.home: HomePage = HomePageFactory(parent=root)  # type: ignore

        site = Site.objects.get()
        site.root_page = self.home
        site.save(update_fields=["root_page"])

        self.rfc_2026 = RFC.objects.create(
            name="draft-ietf-poised95-std-proc-3",
            title="The Internet Standards Process -- Revision 3",
            rfc="2026",
        )

        self.standard_index: StandardIndexPage = StandardIndexPageFactory(
            parent=self.home,
        )  # type: ignore

        self.standard_page: StandardPage = StandardPageFactory(
            parent=self.standard_index,
        )  # type: ignore
        self.standard_page.in_depth = [
            {
                "type": "raw_html",
                "value": (
                    f'<a data-app="snippets" data-id="{self.rfc_2026.pk}"'
                    ' data-linktype="rfc">The Standards RFC</a>'
                ),
            }
        ]
        self.standard_page.save()

    def test_bibliography_item_created(self):
        assert BibliographyItem.objects.count() == 1
        item = BibliographyItem.objects.get()
        assert item.content_object == self.rfc_2026

    def test_referenced_types(self, admin_client):
        rfc_content_type = ContentType.objects.get_for_model(RFC)
        response = admin_client.get(reverse("referenced_types"))
        assert response.status_code == 200
        html = response.content.decode()
        assert reverse("referenced_objects", args=[rfc_content_type.pk]) in html
        assert "snippets | RFC" in html

    def test_referenced_objects(self, admin_client):
        rfc_content_type = ContentType.objects.get_for_model(RFC)
        response = admin_client.get(
            reverse("referenced_objects", args=[rfc_content_type.pk])
        )
        assert response.status_code == 200
        html = response.content.decode()
        assert reverse(
            "referencing_pages", args=[rfc_content_type.pk, self.rfc_2026.pk]
        ) in html
        assert "RFC 2026" in html

    def test_referencing_pages(self, admin_client):
        rfc_content_type = ContentType.objects.get_for_model(RFC)
        response = admin_client.get(
            reverse("referencing_pages", args=[rfc_content_type.pk, self.rfc_2026.pk])
        )
        assert response.status_code == 200
        html = response.content.decode()
        assert self.standard_page.title in html

    def test_render_page(self, client):
        response = client.get(self.standard_page.url)
        assert response.status_code == 200
        html = response.content.decode()
        assert "RFC 2026" in html

    def test_render_page_reference_removed(self, client):
        self.rfc_2026.delete()
        self.standard_page.save()
        response = client.get(self.standard_page.url)
        assert response.status_code == 200
        html = response.content.decode()
        assert "RFC 2026" not in html
        assert "(removed)" in html

    def test_update_fields_partial_raises_exception(self):
        with pytest.raises(ValueError) as error:
            self.standard_page.save(update_fields=["key_info", "in_depth"])

        assert error.match("Either all prepared content fields must be updated or none")

    def test_update_fields_with_all_prepared_fields_succeeds(self):
        self.standard_page.save(
            update_fields=[
                "key_info", "in_depth", "prepared_key_info", "prepared_in_depth"
            ]
        )
