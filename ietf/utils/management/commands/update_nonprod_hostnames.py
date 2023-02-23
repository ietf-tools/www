import os
from logging import Logger

from django.core.management.base import BaseCommand
from wagtail.models import Site

logger = Logger(__name__)


ALLOWED_ENVIRONMENTS = [
    "preview",
    "staging",
]

HOSTNAME_TRANSLATIONS = {
    "www.ietf.org": {
        "preview": "wwwdev.ietf.org",
        "staging": "wwwstaging.ietf.org",
    },
    "www.iab.org": {
        "preview": "iabdev.ietf.org",
        "staging": "iabstaging.ietf.org",
    },
}


class Command(BaseCommand):
    help = "Updates Site objects to have appropriate hostnames for select non-production environments"

    def handle(self, *args, **options):
        # First, make sure we're on the appropriate enviornment.
        environment = os.getenv("ENVIRONMENT")
        if environment not in ALLOWED_ENVIRONMENTS:
            logger.warning("This command is not allowed for this environment.")
            exit()

        # Now adjust hostnames
        all_sites = Site.objects.all()
        for site in all_sites:
            if site.hostname not in HOSTNAME_TRANSLATIONS:
                logger.warning("Site hostname in database is not able to be updated.")
                continue
            new_hostname = HOSTNAME_TRANSLATIONS[site.hostname][environment]
            site.hostname = new_hostname
            site.save()
