import pytest
from wagtail.models import Page, Site

from ietf.home.factories import HomePageFactory


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
