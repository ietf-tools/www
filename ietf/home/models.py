from __future__ import unicode_literals

from datetime import datetime

from django.db import models
from django.db.models.expressions import RawSQL
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.models import Page
from wagtail.search import index

from ietf.blog.models import BlogIndexPage, BlogPage

from ..events.models import EventListingPage, EventPage
from ..topics.models import PrimaryTopicPage, TopicIndexPage
from ..utils.models import RelatedLink


class RequestForCommentsSectionLinks(RelatedLink):
    page = ParentalKey(
        "home.HomePage", related_name="request_for_comments_section_links"
    )


class WorkingGroupsSectionLinks(RelatedLink):
    page = ParentalKey("home.HomePage", related_name="working_groups_section_links")


class HomePage(Page):
    heading = models.CharField(max_length=255)
    introduction = models.CharField(max_length=255, blank=True)
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

    request_for_comments_section_body = models.CharField(max_length=500)
    highlighted_request_for_comment = models.ForeignKey(
        "snippets.RFC",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    working_groups_section_body = models.CharField(max_length=500)
    highlighted_working_group = models.ForeignKey(
        "snippets.WorkingGroup",
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
        index.SearchField("request_for_comments_section_body"),
        index.SearchField("working_groups_section_body"),
    ]

    def topic_index(
        self,
    ):
        return TopicIndexPage.objects.live().first()

    def primary_topics(self):
        try:
            return PrimaryTopicPage.objects.live().descendant_of(self.topic_index())[:3]
        except AttributeError:
            return []

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
        MultiFieldPanel(
            [
                FieldPanel("request_for_comments_section_body"),
                FieldPanel("highlighted_request_for_comment"),
                InlinePanel("request_for_comments_section_links", label="Link"),
            ],
            "Request For Comments Section",
        ),
        MultiFieldPanel(
            [
                FieldPanel("working_groups_section_body"),
                FieldPanel("highlighted_working_group"),
                InlinePanel("working_groups_section_links", label="Link"),
            ],
            "Working Groups Section",
        ),
        FieldPanel("call_to_action"),
    ]


class IABHomePage(Page):
    class Meta:
        verbose_name = "IAB Home Page"

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
            .filter(topics__topic__slug="iab")
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
                FieldPanel("button_text"),
                FieldPanel("main_image"),
                FieldPanel("button_link"),
            ],
            "Header",
        ),
    ]
