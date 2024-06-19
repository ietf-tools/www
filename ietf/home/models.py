from __future__ import unicode_literals

from datetime import datetime
from xml.etree import ElementTree

from django.conf import settings
from django.db import models
from django.db.models.expressions import RawSQL
from requests import get as get_request
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.models import Page
from wagtail.search import index

from ietf.blog.models import BlogIndexPage, BlogPage

from ..announcements.models import IABAnnouncementIndexPage, IABAnnouncementPage
from ..events.models import EventListingPage, EventPage


class HomePage(Page):
    heading = models.CharField(max_length=255)
    introduction = models.CharField(max_length=255)
    main_image = models.ForeignKey(
        "images.IETFImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    button_text = models.CharField(max_length=255, blank=True)
    button_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    call_to_action = models.ForeignKey(
        "snippets.CallToAction",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    search_fields = Page.search_fields + [
        index.SearchField("heading"),
    ]

    def upcoming_events(self):
        return (
            EventPage.objects.filter(end_date__gte=datetime.today())
            .live()
            .order_by("start_date")[:2]
        )

    def event_index(self):
        return EventListingPage.objects.live().first()

    def blog_index(self):
        return BlogIndexPage.objects.live().first()

    def blogs(self, bp_kwargs={}):
        return (
            BlogPage.objects.live()
            .filter(**bp_kwargs)
            .annotate(
                date_sql=RawSQL(
                    "CASE WHEN (date_published IS NOT NULL) THEN date_published ELSE first_published_at END",
                    (),
                )
            )
            .order_by("-date_sql")[:2]
        )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("heading"),
                FieldPanel("introduction"),
                FieldPanel("button_text"),
                FieldPanel("main_image"),
                FieldPanel("button_link"),
            ],
            "Header",
        ),
        FieldPanel("call_to_action"),
    ]


class IABHomePage(Page):
    class Meta:
        verbose_name = "IAB Home Page"

    parent_page_types = ["wagtailcore.Page"]  # Restrict to site root
    subpage_types = settings.IAB_SUBPAGE_TYPES

    heading = models.CharField(max_length=255)
    main_image = models.ForeignKey(
        "images.IETFImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    button_text = models.CharField(max_length=255, blank=True)
    button_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    search_fields = Page.search_fields + [
        index.SearchField("heading"),
    ]

    blog_index_url = settings.IAB_IETF_BLOG_URL

    def announcements(self):
        return IABAnnouncementPage.objects.all().live().order_by("-date")[:2]

    def announcement_index(self):
        return IABAnnouncementIndexPage.objects.live().first()

    def blogs(self, bp_kwargs={}):
        entries = []
        try:
            response = get_request(settings.IAB_FEED_URL)
            xml_data = response.text

            root = ElementTree.fromstring(xml_data)
            for item in root.iter("item"):
                title = item.find("title").text
                description = item.find("description").text
                link = item.find("link").text
                published_date = datetime.strptime(
                    item.find("pubDate").text, "%a, %d %b %Y %H:%M:%S %z"
                )

                entry_data = {
                    "title": title,
                    "description": description,
                    "link": link,
                    "published_date": published_date,
                }
                entries.append(entry_data)
        except Exception as _:
            pass

        return entries

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("heading"),
                FieldPanel("button_text"),
                FieldPanel("main_image"),
                FieldPanel("button_link"),
            ],
            "Header",
        ),
    ]
