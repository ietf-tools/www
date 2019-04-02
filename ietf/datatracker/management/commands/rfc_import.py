from django.core.management.base import BaseCommand
from django.core.mail import mail_admins

from ietf.datatracker.models import RFC


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            RFC.fetch_and_update()
        except Exception as e:
            import traceback
            traceback.print_exc()
            mail_admins("IETF Datatracker %s import failed" % RFC.__name__,
                        e.__repr__())
