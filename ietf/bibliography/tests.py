import pytest
from django.contrib.contenttypes.models import ContentType
from django.test import Client
from django.urls import reverse

from ietf.bibliography.models import BibliographyItem
from ietf.home.models import HomePage
from ietf.snippets.models import RFC
from ietf.standard.factories import StandardIndexPageFactory, StandardPageFactory
from ietf.standard.models import StandardIndexPage, StandardPage

pytestmark = pytest.mark.django_db


class TestBibliography:
    @pytest.fixture(autouse=True)
    def set_up(self, home: HomePage, client: Client):
        self.home = home
        self.client = client

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
        """
        Make sure that a BibliographyItem record was created when
        `self.standard_page` was created in `set_up()`.
        """
        assert BibliographyItem.objects.count() == 1
        item = BibliographyItem.objects.get()
        assert item.content_object == self.rfc_2026

    def test_referenced_types(self, admin_client):
        """
        Admin view that shows which object types might be referenced in content
        pages.
        """
        rfc_content_type = ContentType.objects.get_for_model(RFC)
        response = admin_client.get(reverse("referenced_types"))
        assert response.status_code == 200
        html = response.content.decode()
        assert reverse("referenced_objects", args=[rfc_content_type.pk]) in html
        assert "snippets | RFC" in html

    def test_referenced_objects(self, admin_client):
        """
        Admin view that shows which objects are being referenced as
        bibliography items in content pages.
        """
        rfc_content_type = ContentType.objects.get_for_model(RFC)
        response = admin_client.get(
            reverse("referenced_objects", args=[rfc_content_type.pk])
        )
        assert response.status_code == 200
        html = response.content.decode()
        assert (
            reverse("referencing_pages", args=[rfc_content_type.pk, self.rfc_2026.pk])
            in html
        )
        assert "RFC 2026" in html

    def test_referencing_pages(self, admin_client):
        """
        Admin view that shows which pages are referencing a given object.
        """
        rfc_content_type = ContentType.objects.get_for_model(RFC)
        response = admin_client.get(
            reverse("referencing_pages", args=[rfc_content_type.pk, self.rfc_2026.pk])
        )
        assert response.status_code == 200
        html = response.content.decode()
        assert self.standard_page.title in html

    def test_render_page(self, client):
        """
        The title of the referenced object should be displayed in the page.
        """
        response = client.get(self.standard_page.url)
        assert response.status_code == 200
        html = response.content.decode()
        assert "RFC 2026" in html

    def test_render_page_reference_removed(self, client):
        """
        The target of a BibliographyItem was deleted. It should be displayed as
        such.
        """
        self.rfc_2026.delete()
        self.standard_page.save()
        response = client.get(self.standard_page.url)
        assert response.status_code == 200
        html = response.content.decode()
        assert "RFC 2026" not in html
        assert "(removed)" in html

    def test_update_fields_partial_raises_exception(self):
        """
        Updating the `key_info` and `in_depth` fields, without also updating
        the corresponding `prepared_*` fields, is not allowed. The prepared
        fields contain properly formatted footnotes and are meant to be
        displayed to the visitor.
        """
        with pytest.raises(ValueError) as error:
            self.standard_page.save(update_fields=["key_info", "in_depth"])

        assert error.match("Either all prepared content fields must be updated or none")

    def test_update_fields_with_all_prepared_fields_succeeds(self):
        """
        Updating the `key_info` and `in_depth` fields, while also updating
        the corresponding `prepared_*` fields, should work fine.
        """
        self.standard_page.save(
            update_fields=[
                "key_info",
                "in_depth",
                "prepared_key_info",
                "prepared_in_depth",
            ]
        )
