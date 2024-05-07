from unittest.mock import Mock
import pytest
from wagtail.models import Page, Site

from ietf.home.factories import HomePageFactory, IABHomePageFactory
from ietf.utils.models import IAB_BASE, LayoutSettings


@pytest.fixture(autouse=True)
def disable_caches(settings):
    """
    Tests run with the "dev" settings, which use memcached. We override them
    with the dummy cache so we don't pollute our local development cache.
    """

    settings.CACHES = {
        "default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"},
        "sessions": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"},
        "dummy": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"},
    }


@pytest.fixture
def home():
    site = Site.objects.get()
    site.root_page = HomePageFactory(parent=Page.get_first_root_node())
    site.save(update_fields=["root_page"])
    return site.root_page


@pytest.fixture
def iab_home():
    site = Site.objects.get()
    site.root_page = IABHomePageFactory(parent=Page.get_first_root_node())
    site.hostname = "iab.org"
    site.save(update_fields=["root_page", "hostname"])
    layout_settings = LayoutSettings.for_site(site)
    layout_settings.base_template = IAB_BASE
    layout_settings.save(update_fields=["base_template"])
    return site.root_page


@pytest.fixture(autouse=True)
def iab_blog_feed(monkeypatch: pytest.MonkeyPatch):
    mock_get = Mock()
    mock_get.return_value.text = ""
    monkeypatch.setattr("ietf.home.models.get_request", mock_get)
    return mock_get