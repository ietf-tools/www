from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import (
    FieldPanel, StreamFieldPanel, InlinePanel
)
from wagtail.search import index
from wagtail.snippets.edit_handlers import (
    SnippetChooserPanel
)

from ..utils.models import PromoteMixin, RelatedLink
from ..utils.blocks import StandardBlock


class TopicIndexPage(Page, PromoteMixin):
    """
    This page organises topics. The :model:`topics.PrimaryTopicPage`
    page should be placed beneath it in the page heirarchy.
    """
    introduction = models.CharField(
        max_length=255,
        help_text="Enter the introduction to display on the page, "
        "you can use only 255 characters."
    )

    search_fields = Page.search_fields + [
        index.SearchField('introduction'),
    ]

    subpage_types = ['topics.PrimaryTopicPage',
                    ]

    @property
    def primary_topics(self):
        return PrimaryTopicPage.objects.child_of(self)

    class Meta:
        verbose_name = "Topic Page List"

TopicIndexPage.content_panels = Page.content_panels + [
    FieldPanel('introduction'),
]

TopicIndexPage.promote_panels = Page.promote_panels + PromoteMixin.panels




class PrimaryTopicPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('topics.PrimaryTopicPage',
                       related_name='related_links')


class PrimaryTopicPage(Page, PromoteMixin):
    """
    When this page is saved a :model:`snippets.PrimaryTopic` snippet
    is created. The snippet is used for organising blog posts.
    """
    introduction = models.CharField(
        blank=True,
        max_length=255,
        help_text="Enter the title to display on the page, you can use only 255 characters."
    )
    key_info = StreamField(StandardBlock(required=False), blank=True)
    in_depth = StreamField(StandardBlock(required=False), blank=True)
    call_to_action = models.ForeignKey(
        'snippets.CallToAction',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Will only be displayed if no mailing list signup is selected."
    )
    mailing_list_signup = models.ForeignKey(
        'snippets.MailingListSignup',
        null=True,
        blank=True, on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + [
        index.SearchField('introduction'),
        index.SearchField('key_info'),
        index.SearchField('in_depth'),
    ]

    @property
    def feed_text(self):
        return self.search_description or self.introduction

    @property
    def siblings(self):
        return self.get_siblings().live().public().filter(show_in_menus=True).specific()

    class Meta:
        verbose_name = "Topic Page"


PrimaryTopicPage.content_panels = Page.content_panels + [
    FieldPanel('introduction'),
    StreamFieldPanel('key_info'),
    StreamFieldPanel('in_depth'),
    SnippetChooserPanel('call_to_action'),
    SnippetChooserPanel('mailing_list_signup'),
    InlinePanel('related_links', label="Related Links"),
]

PrimaryTopicPage.promote_panels = Page.promote_panels + PromoteMixin.panels


