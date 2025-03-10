from datetime import datetime

from django.db import models
from modelcluster.fields import ParentalKey
from wagtail import blocks
from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
)
from wagtail.blocks import (
    CharBlock,
    PageChooserBlock,
    StreamBlock,
    StructBlock,
    URLBlock,
)
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail.snippets.blocks import SnippetChooserBlock

from ..snippets.models import Sponsor
from ..utils.blocks import StandardBlock
from ..utils.models import PromoteMixin

# Links


class LinkBlock(StructBlock):
    title = CharBlock()
    link_external = URLBlock(required=False)
    link_page = PageChooserBlock(required=False)
    link_document = DocumentChooserBlock(required=False)

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        if value["link_page"]:
            link = value["link_page"].url
        elif value["link_document"]:
            link = value["link_document"].url
        else:
            link = value["link_external"]
        context.update(link=link, title=value["title"])
        return context

    class Meta:
        template = "events/includes/link_block.html"


class LinkGroupBlock(StreamBlock):
    link = LinkBlock()


class NamedLinkGroupBlock(StructBlock):
    title = CharBlock()
    link_group = LinkGroupBlock()


# Sponsors


class SponsorGroupBlock(StreamBlock):
    sponsor = SnippetChooserBlock(Sponsor)


class SponsorCategoryBlock(StructBlock):
    category_title = CharBlock()
    sponsor_group = SponsorGroupBlock()


# Hosts


class EventPageHost(models.Model):
    page = ParentalKey("events.EventPage", related_name="hosts")
    host = models.ForeignKey(
        "snippets.Sponsor",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [FieldPanel("host")]


# Pages


class EventPage(Page, PromoteMixin):
    """
    A page that describes the IETF's events.

    venue, extras, room_rates, at_a_glance and sponsors are implemented as
    single block streamfields to allow items to be added and removed and to
    allow arbitrary nesting of Panels.
    """

    start_date = models.DateField(
        null=True, blank=True, help_text="The start date date of the event."
    )
    end_date = models.DateField(
        null=True, blank=True, help_text="The end date of the event."
    )
    introduction = models.CharField(
        max_length=511,
        help_text="The introduction for the event page. " "Limited to 511 characters.",
    )
    body = StreamField(StandardBlock(), use_json_field=True)
    main_image = models.ForeignKey(
        "images.IETFImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    venue_section_title = models.CharField(
        max_length=255, default="Meeting venue information", blank=True
    )
    venue = StreamField(
        [("address_line", blocks.CharBlock(classname="full title"))],
        blank=True,
        use_json_field=True,
    )
    extras = StreamField(
        [("extra", blocks.CharBlock(classname="full title"))],
        blank=True,
        use_json_field=True,
    )
    reservation_name = models.CharField(max_length=255, blank=True)
    room_rates = StreamField(
        [
            ("room_rate", blocks.CharBlock(classname="full title")),
            ("table", TableBlock(table_options={"renderer": "html"})),
        ],
        blank=True,
        use_json_field=True,
    )
    reservations_open = models.DateField(null=True, blank=True)
    contact_details = StreamField(
        [("contact_detail", blocks.CharBlock(classname="full title"))],
        blank=True,
        use_json_field=True,
    )

    key_details = StreamField(
        [("item", NamedLinkGroupBlock())], blank=True, use_json_field=True
    )
    key_details_expanded = models.BooleanField(
        default=False,
        help_text="Show the key details items expanded when the page first loads",
    )
    sponsors = StreamField(
        [("sponsor_category", SponsorCategoryBlock())], blank=True, use_json_field=True
    )
    listing_location = models.CharField(
        max_length=255,
        blank=True,
        help_text="Add a short location name to appear on the event listing.",
    )

    @property
    def siblings(self):
        return self.get_siblings().live().public().filter(show_in_menus=True).specific()

    def get_social_image(self):
        return super().get_social_image() or self.main_image

    def get_social_text(self):
        return super().get_social_text() or self.introduction


EventPage.content_panels = Page.content_panels + [
    FieldPanel("start_date"),
    FieldPanel("end_date"),
    FieldPanel("introduction"),
    FieldPanel("body"),
    FieldPanel("main_image"),
    FieldPanel("venue_section_title"),
    FieldPanel("venue"),
    FieldPanel("extras"),
    FieldPanel("reservation_name"),
    FieldPanel("room_rates"),
    FieldPanel("reservations_open"),
    FieldPanel("contact_details"),
    FieldPanel("key_details_expanded"),
    FieldPanel("key_details"),
    InlinePanel("hosts", label="Hosts"),
    FieldPanel("sponsors"),
]

EventPage.promote_panels = (
    Page.promote_panels + PromoteMixin.panels + [FieldPanel("listing_location")]
)


class EventListingPagePromotedEvent(models.Model):
    page = ParentalKey("events.EventListingPage", related_name="promoted_events")
    promoted_event = models.ForeignKey(
        "events.EventPage",
        related_name="+",
        on_delete=models.CASCADE,
    )

    panels = [FieldPanel("promoted_event")]


class EventListingPage(Page, PromoteMixin):
    introduction = models.CharField(blank=True, max_length=511)

    def get_social_text(self):
        return super().get_social_text() or self.introduction

    @property
    def upcoming_events(self):
        return (
            EventPage.objects.filter(end_date__gte=datetime.today())
            .descendant_of(self)
            .live()
            .exclude(
                id__in=self.promoted_events.all().values_list(
                    "promoted_event__id", flat=True
                )
            )
            .order_by("start_date")
        )

    @property
    def past_events(self):
        return (
            EventPage.objects.filter(end_date__lt=datetime.today())
            .descendant_of(self)
            .live()
            .exclude(
                id__in=self.promoted_events.all().values_list(
                    "promoted_event__id", flat=True
                )
            )
            .order_by("-start_date")
        )


EventListingPage.content_panels = Page.content_panels + [
    FieldPanel("introduction"),
    InlinePanel("promoted_events", label="Promoted Events"),
]

EventListingPage.promote_panels = Page.promote_panels + PromoteMixin.panels
