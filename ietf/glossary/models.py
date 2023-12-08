from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.models import Orderable, Page
from wagtail.search.backends import get_search_backend

from ..snippets.models import GlossaryItem
from ..utils.models import PromoteMixin, RelatedLink


class GlossaryPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey("glossary.GlossaryPage", related_name="related_links")


class GlossaryPage(Page, PromoteMixin):
    """
    This page lists all :models:`snippets.GlossaryItem` snippets.
    """

    introduction = models.CharField(
        blank=True,
        max_length=511,
        help_text="The page introduction text. You can only use 511 characters.",
    )
    call_to_action = models.ForeignKey(
        "snippets.CallToAction",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    mailing_list_signup = models.ForeignKey(
        "snippets.MailingListSignup",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    def get_social_text(self):
        return super().get_social_text() or self.introduction

    @property
    def siblings(self):
        return self.get_siblings().live().public().filter(show_in_menus=True).specific()

    def get_context(self, request, *args, **kwargs):
        context = super(GlossaryPage, self).get_context(request, *args, **kwargs)
        glossary_items = GlossaryItem.objects.all()

        if request.GET.get("query"):
            s = get_search_backend()
            glossary_items = s.search(request.GET.get("query"), glossary_items)

        context["glossary_items"] = {}
        for item in glossary_items:
            if item.title[0:1].upper() not in context["glossary_items"].keys():
                context["glossary_items"][item.title[0:1].upper()] = [item]
            else:
                context["glossary_items"][item.title[0:1].upper()].append(item)
        context["search_query"] = request.GET.get("query")

        return context


GlossaryPage.content_panels = Page.content_panels + [
    FieldPanel("introduction"),
    InlinePanel("related_links", label="Related Links"),
    FieldPanel("call_to_action"),
    FieldPanel("mailing_list_signup"),
]

GlossaryPage.promote_panels = Page.promote_panels + PromoteMixin.panels
