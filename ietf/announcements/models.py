from django.conf import settings
from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
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
    introduction = models.CharField(
        blank=True,
        max_length=255,
        help_text="Enter the title to display on the page, "
        "you can use only 255 characters.",
    )
    body = StreamField(StandardBlock(), use_json_field=True)

    search_fields = Page.search_fields + [
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("introduction"),
        FieldPanel("body"),
    ]


class IABAnnouncementIndexPage(Page):
    """
    An index for IAB Announcements.
    """

    class Meta:
        verbose_name = "IAB Announcement Index Page"

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

    search_fields = Page.search_fields + [
        index.SearchField("introduction"),
    ]

    @property
    def children(self):
        announcements = self.get_children().live().specific()
        return sorted(announcements, key=lambda announcement: announcement.specific.date, reverse=True)


IABAnnouncementIndexPage.content_panels = Page.content_panels + [
    FieldPanel("introduction"),
]
