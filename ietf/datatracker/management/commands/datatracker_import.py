from django.core.management.base import BaseCommand
from django.core.mail import mail_admins

from ietf.datatracker.models import DatatrackerMixin


class Command(BaseCommand):
    def handle(self, *args, **options):
        for cls in DatatrackerMixin.__subclasses__():
            try:
                print("fetching {}".format(cls.__module__ + "." + cls.__name__))
                ct = cls.fetch_and_update()
                print("  fetched {} items".format(ct))
            except Exception as e:
                import traceback
                traceback.print_exc()
                mail_admins("IETF Datatracker %s import failed" % cls.__name__,
                            e.__repr__())
