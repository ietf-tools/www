# Copyright The IETF Trust 2007-2024, All Rights Reserved
# -*- coding: utf-8 -*-

from email.utils import parseaddr
import os

def _multiline_to_list(s):
    """Helper to split at newlines and conver to list"""
    return [item.strip() for item in s.split("\n")]


DEFAULT_FROM_EMAIL = "donotreply@ietf.org"
SERVER_EMAIL = "donotreply@ietf.org"
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("IETFWWW_EMAIL_HOST", "localhost")
EMAIL_PORT = int(os.environ.get("IETFWWW_EMAIL_PORT", "2025"))

# Default to "development". Production _must_ set IETFWWW_SERVER_MODE="production" in the env!
SERVER_MODE = os.environ.get("IETFWWW_SERVER_MODE", "development")

# Secrets
_SECRET_KEY = os.environ.get("IETFWWW_DJANGO_SECRET_KEY", None)
if _SECRET_KEY is not None:
    SECRET_KEY = _SECRET_KEY
else:
    raise RuntimeError("IETFWWW_DJANGO_SECRET_KEY must be set")


_CSRF_TRUSTED_ORIGINS_STR = os.environ.get("IETFWWW_CSRF_TRUSTED_ORIGINS", None)
if _CSRF_TRUSTED_ORIGINS_STR is not None:
    CSRF_TRUSTED_ORIGINS = _multiline_to_list(_CSRF_TRUSTED_ORIGINS_STR)

FILE_UPLOAD_PERMISSIONS = 0o664
_WAGTAILADMIN_BASE_URL = os.environ.get("WAGTAILADMIN_BASE_URL", None)
if _WAGTAILADMIN_BASE_URL is not None:
    WAGTAILADMIN_BASE_URL = _WAGTAILADMIN_BASE_URL
else:
    raise RuntimeError("WAGTAILADMIN_BASE_URL must be present")

# Set DEBUG if IETFWWW_DEBUG env var is the word "true"
DEBUG = os.environ.get("IETFWWW_DEBUG", "false").lower() == "true"

# IETFWWW_ALLOWED_HOSTS env var is a comma-separated list of allowed hosts
_ALLOWED_HOSTS_STR = os.environ.get("IETFWWW_ALLOWED_HOSTS", None)
if _ALLOWED_HOSTS_STR is not None:
    ALLOWED_HOSTS = _multiline_to_list(_ALLOWED_HOSTS_STR)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "HOST": os.environ.get("IETFWWW_DB_HOST", "db"),
        "PORT": os.environ.get("IETFWWW_DB_PORT", "5432"),
        "NAME": os.environ.get("IETFWWW_DB_NAME", "ietfweb"),
        "USER": os.environ.get("IETFWWW_DB_USER", "django"),
        "PASSWORD": os.environ.get("IETFWWW_DB_PASS", ""),
        "CONN_MAX_AGE": 600,  # number of seconds database connections should persist for
    },
}

# IETFWWW_ADMINS is a newline-delimited list of addresses parseable by email.utils.parseaddr
_admins_str = os.environ.get("IETFWWW_ADMINS", None)
if _admins_str is not None:
    ADMINS = [parseaddr(admin) for admin in _multiline_to_list(_admins_str)]
else:
    raise RuntimeError("IETFWWW_ADMINS must be set")

# Leave IETFWWW_MATOMO_SITE_ID unset to disable Matomo reporting
if "IETFWWW_MATOMO_SITE_ID" in os.environ:
    MATOMO_DOMAIN_PATH = os.environ.get("IETFWWW_MATOMO_DOMAIN_PATH", "analytics.ietf.org")
    MATOMO_SITE_ID = os.environ.get("IETFWWW_MATOMO_SITE_ID", None)
    MATOMO_DISABLE_COOKIES = True

# Duplicating production cache from settings.py and using it whether we're in production mode or not
MEMCACHED_HOST = os.environ.get("IETFWWW_MEMCACHED_SERVICE_HOST", "127.0.0.1")
MEMCACHED_PORT = os.environ.get("IETFWWW_MEMCACHED_SERVICE_PORT", "11211")
MEMCACHED_KEY_PREFIX = "ietf"
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
        "LOCATION": f"{MEMCACHED_HOST}:{MEMCACHED_PORT}",
        "KEY_PREFIX": MEMCACHED_KEY_PREFIX,
    },
    "sessions": {
        "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
        "LOCATION": f"{MEMCACHED_HOST}:{MEMCACHED_PORT}",
        "KEY_PREFIX": MEMCACHED_KEY_PREFIX,
    },
    "dummy": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"},
}

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
