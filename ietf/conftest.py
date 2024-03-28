import pytest


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
