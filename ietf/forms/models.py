from logging import Logger

from django.contrib import messages
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.fields import RichTextField

logger = Logger(__name__)


class EmailException(Exception):
    def __init__(self, message="Error sending email", code=500, params=None):
        super().__init__(message, code, params)
        self.message = message
        self.code = code


class FormField(AbstractFormField):
    page = ParentalKey("FormPage", related_name="form_fields")

    @classmethod
    def _migrate_legacy_clean_name(cls):
        return None


class FormPage(AbstractEmailForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    def send_mail(self, form):
        try:
            super().send_mail(form)
        except Exception as ex:
            logger.error(f"Failed to send email with exception: {ex}")
            raise EmailException from ex

    def serve(self, request, *args, **kwargs):
        try:
            return super().serve(request, *args, **kwargs)
        except EmailException:
            messages.add_message(
                request, messages.ERROR, message="Failed to send email"
            )
            raise


FormPage.content_panels = [
    FieldPanel("title", classname="title"),
    FieldPanel("intro"),
    InlinePanel("form_fields", label="Form fields"),
    FieldPanel("thank_you_text"),
    MultiFieldPanel(
        [
            FieldPanel("to_address"),
            FieldPanel("from_address"),
            FieldPanel("subject"),
        ],
        "Email",
    ),
]
