from logging import Logger

from django.contrib import messages
from django.views.defaults import server_error
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.core.fields import RichTextField

from ietf.views import server_error

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
            logger.error("Failed to send email with exception: {}".format(ex))
            raise EmailException

    def serve(self, request, *args, **kwargs):
        try:
            return super().serve(request, *args, **kwargs)
        except EmailException as Ex:
            messages.add_message(
                request, messages.ERROR, message="Failed to send email"
            )
            raise EmailException


FormPage.content_panels = [
    FieldPanel("title", classname="full title"),
    FieldPanel("intro", classname="full"),
    InlinePanel("form_fields", label="Form fields"),
    FieldPanel("thank_you_text", classname="full"),
    MultiFieldPanel(
        [
            FieldPanel("to_address", classname="full"),
            FieldPanel("from_address", classname="full"),
            FieldPanel("subject", classname="full"),
        ],
        "Email",
    ),
]
