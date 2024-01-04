import os
import sys

from .base import *

# Do not set SECRET_KEY, Postgres or LDAP password or any other sensitive data here.
# Instead, create a local.py file on the server.

# Disable debug mode
DEBUG = False


# Configuration from environment variables
# Alternatively, you can set these in a local.py file on the server

env = os.environ.copy()

# On Torchbox servers, many environment variables are prefixed with "CFG_"
for key, value in os.environ.items():
    if key.startswith('CFG_'):
        env[key[4:]] = value


# Basic configuration

APP_NAME = env.get('APP_NAME', 'ietf')

if 'SECRET_KEY' in env:
    SECRET_KEY = env['SECRET_KEY']

if 'ALLOWED_HOSTS' in env:
    ALLOWED_HOSTS = env['ALLOWED_HOSTS'].split(',')

if 'CSRF_TRUSTED_ORIGINS' in env:
    CSRF_TRUSTED_ORIGINS = env['CSRF_TRUSTED_ORIGINS'].split(',')

if 'PRIMARY_HOST' in env:
    WAGTAILADMIN_BASE_URL = 'http://%s/' % env['PRIMARY_HOST']

if 'SERVER_EMAIL' in env:
    SERVER_EMAIL = env['SERVER_EMAIL']

if 'CACHE_PURGE_URL' in env:
    INSTALLED_APPS += ( 'wagtail.contrib.frontend_cache', )
    WAGTAILFRONTENDCACHE = {
        'default': {
            'BACKEND': 'wagtail.contrib.frontend_cache.backends.HTTPBackend',
            'LOCATION': env['CACHE_PURGE_URL'],
        },
    }

if 'STATIC_URL' in env:
    STATIC_URL = env['STATIC_URL']

if 'STATIC_DIR' in env:
    STATIC_ROOT = env['STATIC_DIR']

if 'MEDIA_URL' in env:
    MEDIA_URL = env['MEDIA_URL']

if 'MEDIA_DIR' in env:
    MEDIA_ROOT = env['MEDIA_DIR']

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env.get('PGDATABASE', APP_NAME),
        'CONN_MAX_AGE': 600,  # number of seconds database connections should persist for

        # User, host and port can be configured by the PGUSER, PGHOST and
        # PGPORT environment variables (these get picked up by libpq).
    }
}

# Caches

if 'CACHE_DEFAULT' in env:
    CACHES['default']['LOCATION'] = env.get('CACHE_DEFAULT')

if 'CACHE_SESSIONS' in env:
    CACHES['sessions']['LOCATION'] = env.get('CACHE_SESSIONS')


# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers':     ['mail_admins'],
            'level':        'ERROR',
            'propagate':    False,
        },
        'django.security': {
            'handlers':     ['mail_admins'],
            'level':        'ERROR',
            'propagate':    False,
        },
    },
}


# Log errors to file
if 'ERROR_LOG' in env:
    LOGGING['handlers']['errors_file'] = {
        'level':        'ERROR',
        'class':        'logging.handlers.RotatingFileHandler',
        'filename':     env['ERROR_LOG'],
        'maxBytes':     5242880, # 5MB
        'backupCount':  5
    }
    LOGGING['loggers']['django.request']['handlers'].append('errors_file')
    LOGGING['loggers']['django.security']['handlers'].append('errors_file')

try:
    from .local import *    # pyflakes:ignore
except ImportError:
    pass
