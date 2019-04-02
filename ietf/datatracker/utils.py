from redlock import RedLockFactory

from django.conf import settings


def get_redlock():
    redis_url = getattr(settings, 'REDIS_LOCATION', '127.0.0.1:6379')

    return RedLockFactory([
        {'url': redis_url}
    ])
