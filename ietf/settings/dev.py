import contextlib

from .base import *  # noqa: F403

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "CHANGEME!!!"


EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# Process all tasks synchronously.
# Helpful for local development and running tests
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
CELERY_ALWAYS_EAGER = True

with contextlib.suppress(ImportError):
    from .local import *  # noqa: F403
