from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import StreamField
from wagtail.models import Orderable, Page
from wagtail.search import index

from ..utils.blocks import StandardBlock
from ..utils.models import PromoteMixin, RelatedLink


class TopicIndexPage(Page, PromoteMixin):
    """
    This page organises topics. The :model:`topics.PrimaryTopicPage`
    page should be placed beneath it in the page heirarchy.
    """

    introduction = models.CharField(
        max_length=255,
        help_text="Enter the introduction to display on the page, "
        "you can use only 255 characters.",
    )

    search_fields = Page.search_fields + [
        index.SearchField("introduction"),
    ]

    subpage_types = [
        "topics.PrimaryTopicPage",
    ]

    def get_social_text(self):
        return super().get_social_text() or self.introduction

    @property
    def primary_topics(self):
        return PrimaryTopicPage.objects.child_of(self)

    class Meta:
        verbose_name = "Topic Page List"


TopicIndexPage.content_panels = Page.content_panels + [
    FieldPanel("introduction"),
]

TopicIndexPage.promote_panels = Page.promote_panels + PromoteMixin.panels


class PrimaryTopicPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey("topics.PrimaryTopicPage", related_name="related_links")


class PrimaryTopicPage(Page, PromoteMixin):
    """
    When this page is saved a :model:`snippets.PrimaryTopic` snippet
    is created. The snippet is used for organising blog posts.
    """

    introduction = models.CharField(
        blank=True,
        max_length=255,
        help_text="Enter the title to display on the page, you can use only 255 characters.",
    )
    key_info = StreamField(StandardBlock(required=False), blank=True, use_json_field=True)
    in_depth = StreamField(StandardBlock(required=False), blank=True, use_json_field=True)
    call_to_action = models.ForeignKey(
        "snippets.CallToAction",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Will only be displayed if no mailing list signup is selected.",
    )
    mailing_list_signup = models.ForeignKey(
        "snippets.MailingListSignup",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    search_fields = Page.search_fields + [
        index.SearchField("introduction"),
        index.SearchField("key_info"),
        index.SearchField("in_depth"),
    ]

    def get_social_text(self):
        return super().get_social_text() or self.introduction

    @property
    def siblings(self):
        return self.get_siblings().live().public().filter(show_in_menus=True).specific()

    class Meta:
        verbose_name = "Topic Page"


PrimaryTopicPage.content_panels = Page.content_panels + [
    FieldPanel("introduction"),
    FieldPanel("key_info"),
    FieldPanel("in_depth"),
    FieldPanel("call_to_action"),
    FieldPanel("mailing_list_signup"),
    InlinePanel("related_links", label="Related Links"),
]

PrimaryTopicPage.promote_panels = Page.promote_panels + PromoteMixin.panels
