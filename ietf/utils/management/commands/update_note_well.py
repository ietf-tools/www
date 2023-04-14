from logging import Logger

import markdown
import requests
from django.conf import settings
from django.core.management.base import BaseCommand

from ietf.utils.models import TextChunk

logger = Logger(__name__)


class Command(BaseCommand):
    help = "Update the note well text chunk from the note well github repo"

    def handle(self, *args, **options):
        # Get content from github
        note_well_url = settings.NOTE_WELL_REPO
        response = requests.get(note_well_url)
        if response.status_code != 200:
            logger.warn(
                f"Error retrieving latest note well data - response code {response.status_code} received when querying {note_well_url}"
            )
            return

        # Convert from markdown to HTML
        repo_content = response.content.decode("utf-8")
        html_for_page = markdown.markdown(repo_content)

        # Update note well page
        note_well, created = TextChunk.objects.get_or_create(slug="note-well")
        note_well.text = html_for_page
        note_well.save()
        logger.info("Note well text chunk updated")
