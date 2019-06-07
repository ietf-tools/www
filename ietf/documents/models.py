from django.db import models

from wagtail.documents.models import Document

class IetfDocument(Document):

    @property
    def url(self):
        return self.file.url
