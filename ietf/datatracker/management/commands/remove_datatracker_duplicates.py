from django.core.management.base import BaseCommand

from wagtail.admin import utils

from ietf.datatracker import models


class Command(BaseCommand):
    """
    Delete all duplicated Datatracker objects that have not been used in a page.
    """
    def handle(self, *args, **options):
        for cls in models.DatatrackerMixin.__subclasses__():
            for instance in cls.objects.all():
                duplicates = cls.objects.filter(
                    **{cls.IDENTIFIER: getattr(instance, cls.IDENTIFIER)}
                )
                if duplicates.count() > 1:
                    for duplicate in duplicates:
                        usage = utils.get_object_usage(duplicate)
                        if usage.count() < 1:
                            duplicate.delete()
