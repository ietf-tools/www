from unittest.mock import Mock, call

import pytest
from django.core.management import call_command
from django.test import Client
from wagtail.models import Page

from ietf.home.models import HomePage
from ietf.standard.factories import StandardIndexPageFactory, StandardPageFactory
from ietf.standard.models import StandardIndexPage, StandardPage
from ietf.utils.models import MainMenuItem

pytestmark = pytest.mark.django_db


class TestPagePurging:
    @pytest.fixture(autouse=True)
    def set_up(self, home: HomePage, client: Client, monkeypatch: pytest.MonkeyPatch):
        self.home = home
        self.client = client

        self.standard_index: StandardIndexPage = StandardIndexPageFactory(
            parent=self.home,
        )  # type: ignore

        self.standard_page: StandardPage = StandardPageFactory(
            parent=self.standard_index,
        )  # type: ignore

        self.mock_purge = Mock()
        monkeypatch.setattr(
            "ietf.utils.signal_handlers.purge_pages_from_cache", self.mock_purge
        )

    def test_purge_parent(self):
        self.standard_page.save_revision().publish()

        # Wagtail already purges the page itself
        assert self.mock_purge.call_args_list == [
            call({Page.objects.get(pk=self.standard_index.pk)}),
        ]

    def test_purge_referencing_page(self):
        self.standard_page.key_info = [
            {
                "type": "paragraph",
                "value": f'<p><a id="{self.home.pk}" linktype="page">Home</a></p>',
            },
        ]
        self.standard_page.save()
        call_command("rebuild_references_index", verbosity=0)
        self.home.save_revision().publish()

        # Wagtail already purges the page itself
        assert self.mock_purge.call_args_list == [
            call({Page.objects.get(pk=self.standard_page.pk)}),
        ]

    def test_main_menu_item_updates_homepage(self):
        MainMenuItem.objects.create(page=self.standard_page, sort_order=1)

        assert self.mock_purge.call_args_list == [
            call({Page.objects.get(pk=self.home.pk)}),
        ]

    def test_main_menu_reference_updates_homepage(self):
        MainMenuItem.objects.create(page=self.standard_page, sort_order=1)
        self.mock_purge.reset_mock()
        call_command("rebuild_references_index", verbosity=0)
        self.standard_page.save_revision().publish()

        assert self.mock_purge.call_args_list == [
            call(
                {
                    Page.objects.get(pk=self.home.pk),
                    # parent page gets purged anyway
                    Page.objects.get(pk=self.standard_index.pk),
                }
            ),
        ]
