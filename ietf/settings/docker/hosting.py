from .base import *

from .grains.aws import *

SECURE_HSTS_SECONDS = 31536000
CACHE_MIDDLEWARE_ALIAS = "dummy" # Remove after upgrade to Wagtail >= 2.10. See https://github.com/wagtail/wagtail/issues/5975
