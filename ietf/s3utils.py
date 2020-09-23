import mimetypes

from django.conf import settings
from django.utils.functional import LazyObject
from storages.backends.s3boto3 import S3Boto3Storage

mimetypes.add_type("application/font-woff", "woff", strict=True)
mimetypes.add_type("application/font-woff", "woff2", strict=True)


class StaticRootS3BotoStorage(LazyObject):
    def _setup(self):
        self._wrapped = S3Boto3Storage(
            location="static/{}".format(
                getattr(settings, "APPLICATION_VERSION", "")
            ).strip("/")
        )


class MediaRootS3BotoStorage(LazyObject):
    def _setup(self):
        self._wrapped = S3Boto3Storage(location="media")
