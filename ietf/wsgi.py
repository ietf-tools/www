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
    django_application = get_wsgi_application()

    return django_application(environ, start_response)
