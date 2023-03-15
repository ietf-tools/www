from django.conf import settings
from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page
from wagtail.search import index

from ..utils.blocks import StandardBlock


class IABAnnouncementPage(Page):
    """
    A simple page for announcements.
    """

    class Meta:
        verbose_name = "IAB Announcement Page"

    parent_page_types = [
        "announcements.IABAnnouncementIndexPage",
    ]
    subpage_types = []

    date = models.DateTimeField()
    introduction = RichTextField()
    body = StreamField(StandardBlock(), use_json_field=True)

    search_fields = Page.search_fields + [
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("introduction"),
        FieldPanel("body"),
        InlinePanel("topics", label="Topics"),
    ]


class IABAnnouncementIndexPage(Page):
    """
    An index for IAB Announcements.
    """

    parent_page_types = settings.IAB_PARENT_PAGE_TYPES
    subpage_types = [
        "announcements.IABAnnouncementPage",
    ]

    introduction = models.CharField(
        blank=True,
        max_length=255,
        help_text="Enter the title to display on the page, "
        "you can use only 255 characters.",
    )
    key_info = StreamField(
        StandardBlock(required=False), blank=True, use_json_field=True
    )
    in_depth = StreamField(
        StandardBlock(required=False), blank=True, use_json_field=True
    )

    search_fields = Page.search_fields + [
        index.SearchField("introduction"),
        index.SearchField("key_info"),
        index.SearchField("in_depth"),
    ]

    @property
    def children(self):
        return self.get_children().live().specific()

    class Meta:
        verbose_name = "IAB Announcement Index Page"


IABAnnouncementIndexPage.content_panels = Page.content_panels + [
    FieldPanel("introduction"),
    FieldPanel("key_info"),
    FieldPanel("in_depth"),
]


class IABAnnouncementTopic(models.Model):
    """
    A through model from :model:`announcements.IABAnnouncementPage`
    to :model:`snippets.Topic`
    """

    page = ParentalKey("announcements.IABAnnouncementPage", related_name="topics")
    topic = models.ForeignKey(
        "snippets.Topic",
        related_name="+",
        on_delete=models.CASCADE,
    )

    panels = [FieldPanel("topic")]
