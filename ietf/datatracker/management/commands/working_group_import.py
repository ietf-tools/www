from django.core.management.base import BaseCommand
from django.core.mail import mail_admins

from ietf.datatracker.models import WorkingGroup


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            print("importing WorkingGroups")
            ct = WorkingGroup.fetch_and_update()
            print("  imported {} elements".format(ct))
        except Exception as e:
            mail_admins("IETF Datatracker %s import failed" % WorkingGroup.__name__,
                        e.__repr__())
