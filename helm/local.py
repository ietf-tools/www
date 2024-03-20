import os

DEFAULT_FROM_EMAIL = "donotreply@ietf.org"
SERVER_EMAIL = "donotreply@ietf.org"
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ["EMAIL_HOST"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "HOST": os.environ["DBHOST"],
        "NAME": os.environ["DBNAME"],
        "USER": os.environ["DBUSER"],
        "PASSWORD": os.environ["DBPASS"],
        "CONN_MAX_AGE": 600,  # number of seconds database connections should persist for
    },
}

SECRET_KEY = os.environ["SECRET_KEY"]

FILE_UPLOAD_PERMISSIONS = 0o664

ALLOWED_HOSTS = os.environ["ALLOWED_HOSTS"].split(",")

WAGTAILADMIN_BASE_URL = os.environ["WAGTAILADMIN_BASE_URL"]

ADMINS = (("Django Server", "django-project@ietf.org"),)

# Logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": False,
        },
        "django.security": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}

MATOMO_DOMAIN_PATH = "analytics.ietf.org"
MATOMO_SITE_ID = "1"
MATOMO_DISABLE_COOKIES = True

MEMCACHED_HOST = os.environ["MEMCACHED_SERVICE_HOST"]
MEMCACHED_PORT = os.environ["MEMCACHED_SERVICE_PORT"]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
        "LOCATION": f"{MEMCACHED_HOST}:{MEMCACHED_PORT}",
        "KEY_PREFIX": "ietf",
    },
    "sessions": {
        "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
        "LOCATION": f"{MEMCACHED_HOST}:{MEMCACHED_PORT}",
        "KEY_PREFIX": "ietf",
    },
    "dummy": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"},
}
