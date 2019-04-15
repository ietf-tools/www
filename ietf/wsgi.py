"""
WSGI config for ietf project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ietf.settings.production")


def application(environ, start_response):
    # This block was from an earlier attempt to manage config via environment variables
    #try:
    #    os.environ['DJANGO_SETTINGS_MODULE'] = environ['DJANGO_SETTINGS_MODULE']
    #    os.environ['CFG_SECRET_KEY'] = environ['CFG_SECRET_KEY']
    #    os.environ['CFG_ALLOWED_HOSTS'] = environ['CFG_ALLOWED_HOSTS']
    #    os.environ['CFG_STATIC_URL'] = environ['CFG_STATIC_URL']
    #    os.environ['CFG_STATIC_DIR'] = environ['CFG_STATIC_DIR']
    #    os.environ['CFG_MEDIA_URL'] = environ['CFG_MEDIA_URL']
    #    os.environ['CFG_MEDIA_DIR'] = environ['CFG_MEDIA_DIR']
    #    os.environ['CFG_APP_NAME'] = environ['CFG_APP_NAME']
    #    os.environ['PGUSER'] = environ['PGUSER']
    #    os.environ['PGHOST'] = environ['PGHOST']
    #    os.environ['PGDATABASE'] = environ['PGDATABASE']
    #    os.environ['CFG_SERVER_EMAIL'] = environ['CFG_SERVER_EMAIL']
    #    os.environ['CFG_ERROR_LOG'] = environ['CFG_ERROR_LOG']
    #except KeyError as e:
    #    print("At least one environment variable not set: %s" % e)

    django_application = get_wsgi_application()

    return django_application(environ, start_response)
