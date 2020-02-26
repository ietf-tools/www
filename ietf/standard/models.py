from collections import OrderedDict

from django.db import models

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import (
    FieldPanel, StreamFieldPanel, InlinePanel
)
from wagtail.snippets.edit_handlers import (
    SnippetChooserPanel,
)
from wagtail.search import index

from modelcluster.fields import ParentalKey

from ..utils.models import PromoteMixin, RelatedLink
from ..utils.blocks import StandardBlock
from ..bibliography.models import BibliographyMixin


class StandardPageFAQItem(Orderable, models.Model):
    """
    A question and answer pair that can be added to a Standard
    Page.
    """
    page = ParentalKey('standard.StandardPage',
                       related_name='faq_items')
    question = models.TextField()
    answer = models.TextField()

    panels = [
        FieldPanel('question'),
        FieldPanel('answer')
    ]


class StandardPageFeedRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('standard.StandardPage',
                       related_name='feed_related_links')


class StandardPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('standard.StandardPage', related_name='related_links')


class StandardPage(Page, BibliographyMixin, PromoteMixin):
    introduction = models.CharField(
        blank=True,
        max_length=255,
        help_text="Enter the title to display on the page, "
        "you can use only 255 characters."
    )
    key_info = StreamField(StandardBlock(required=False), blank=True)
    in_depth = StreamField(StandardBlock(required=False), blank=True)
    call_to_action = models.ForeignKey(
        'snippets.CallToAction',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Specify the page you would like visitors to go to next."
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

    # for bibliography
    prepared_key_info = models.TextField(
        blank=True, null=True,
        help_text="The prepared key info field after bibliography styling has been applied. Auto-generated on each save.",
    )
    prepared_in_depth = models.TextField(
        blank=True, null=True,
        help_text="The prepared in depth field after bibliography styling has been applied. Auto-generated on each save.",
    )
    CONTENT_FIELD_MAP = OrderedDict([
        ('key_info', 'prepared_key_info'),
        ('in_depth', 'prepared_in_depth'),
    ])

    @property
    def feed_text(self):
        return self.search_description or self.introduction

    @property
    def siblings(self):
        return self.get_siblings().live().public().filter(show_in_menus=True).specific()

    def serve_preview(self, request, mode_name):
        """ This is another hack to overcome the MRO issue we were seeing """
        return BibliographyMixin.serve_preview(self, request, mode_name)


StandardPage.content_panels = Page.content_panels + [
    FieldPanel('introduction'),
    StreamFieldPanel('key_info'),
    StreamFieldPanel('in_depth'),
    SnippetChooserPanel('call_to_action'),
    SnippetChooserPanel('mailing_list_signup'),
    InlinePanel('related_links', label="Related Links"),
    InlinePanel('faq_items', label="FAQ Items"),
]

StandardPage.promote_panels = Page.promote_panels + PromoteMixin.panels + [
    InlinePanel('feed_related_links', label="Feed related Links"),
]


class StandardIndexPage(Page, PromoteMixin):
    """
    An index for standard pages.
    """
    introduction = models.CharField(
        blank=True,
        max_length=255,
        help_text="Enter the title to display on the page, "
        "you can use only 255 characters."
    )
    key_info = StreamField(StandardBlock(required=False), blank=True)
    in_depth = StreamField(StandardBlock(required=False), blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('introduction'),
        index.SearchField('key_info'),
        index.SearchField('in_depth'),
    ]

    @property
    def children(self):
        return self.get_children().live().specific()

    class Meta:
        verbose_name = "Index Page"


StandardIndexPage.content_panels = Page.content_panels + [
    FieldPanel('introduction'),
    StreamFieldPanel('key_info'),
    StreamFieldPanel('in_depth'),
]

StandardIndexPage.promote_panels = Page.promote_panels + PromoteMixin.panels
