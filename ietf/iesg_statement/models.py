from datetime import datetime, time
from functools import partial

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.functions import Coalesce
from django.shortcuts import redirect
from django.utils import functional
from django.utils.safestring import mark_safe
from django.utils.timezone import make_aware
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail.search import index

from ..bibliography.models import BibliographyMixin
from ..snippets.models import Topic
from ..utils.blocks import StandardBlock
from ..utils.models import PromoteMixin


def make_date_aware(value):
    return make_aware(datetime.combine(value, time()))


def filter_pages_by_topic(pages, topic):
    return pages.filter(topics__topic=topic)


def get_topic_by_id(id):
    return Topic.objects.get(id=id)


def filter_pages_by_date_from(pages, date_from):
    return pages.filter(d__gte=make_date_aware(date_from))


def filter_pages_by_date_to(pages, date_to):
    return pages.filter(d__lte=make_date_aware(date_to))


def parse_date_search_input(date):
    return datetime.date(datetime.strptime(date, "%d/%m/%Y"))


def build_filter_text(**kwargs):
    if any(kwargs):
        text_fragments = []
        if kwargs.get("topic"):
            text_fragments.append("<span>{}</span>".format(kwargs.get("topic")))
        if kwargs.get("date_from") and kwargs.get("date_to"):
            text_fragments.append(
                "dates between <span>{}</span> &amp; <span>{}</span>".format(
                    kwargs["date_from"], kwargs["date_to"]
                )
            )
        elif kwargs.get("date_from"):
            text_fragments.append(
                "dates after <span>{}</span>".format(kwargs["date_from"])
            )
        elif kwargs.get("date_to"):
            text_fragments.append(
                "dates before <span>{}</span>".format(kwargs["date_to"])
            )
        return ", ".join(text_fragments)
    else:
        return ""


parameter_functions_map = {
    "topic": [get_topic_by_id, filter_pages_by_topic],
    "date_from": [parse_date_search_input, filter_pages_by_date_from],
    "date_to": [parse_date_search_input, filter_pages_by_date_to],
}


class IESGStatementTopic(models.Model):

    page = ParentalKey("iesg_statement.IESGStatementPage", related_name="topics")
    topic = models.ForeignKey(
        "snippets.Topic",
        related_name="+",
        on_delete=models.CASCADE,
    )

    panels = [FieldPanel("topic")]


class IESGStatementPage(Page, BibliographyMixin, PromoteMixin):

    date_published = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Use this field to override the date that the "
        "blog post appears to have been published.",
    )
    introduction = models.CharField(
        max_length=511, help_text="The page introduction text."
    )
    body = StreamField(StandardBlock(), use_json_field=True)

    search_fields = Page.search_fields + [
        index.SearchField("introduction"),
        index.SearchField("body"),
    ]

    # for bibliography
    prepared_body = models.TextField(
        blank=True,
        null=True,
        help_text="The prepared body content after bibliography styling has been applied. Auto-generated on each save.",
    )
    CONTENT_FIELD_MAP = {"body": "prepared_body"}

    parent_page_types = ["iesg_statement.IESGStatementIndexPage"]
    subpage_types = []

    def get_social_text(self):
        return super().get_social_text() or self.introduction

    @property
    def date(self):
        return self.date_published or self.first_published_at

    @property
    def next(self):
        if not self.date:
            return None
        after = sorted(
            [p for p in self.siblings.exclude(pk=self.pk) if p.date > self.date],
            key=lambda o: o.date,
        )
        return after and after[0] or None

    @property
    def previous(self):
        if not self.date:
            return None
        before = sorted(
            [p for p in self.siblings.exclude(pk=self.pk) if p.date < self.date],
            key=lambda o: o.date,
            reverse=True,
        )
        return before and before[0] or None

    def coalesced_published_date(self):
        return self.date_published or self.first_published_at

    @functional.cached_property
    def siblings(self):
        return (
            self.__class__.objects.live()
            .sibling_of(self)
            .annotate(d=Coalesce("date_published", "first_published_at"))
            .order_by("-d")
        )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        siblings = self.siblings
        query_string = "?"
        filter_text_builder = build_filter_text

        for parameter, functions in parameter_functions_map.items():
            search_query = request.GET.get(parameter)
            if search_query:
                try:
                    related_object = functions[0](search_query)
                    siblings = functions[1](siblings, related_object)
                    query_string += f"{parameter}={search_query}&"
                    filter_text_builder = partial(
                        filter_text_builder, **{parameter: related_object.__str__()}
                    )
                except (ValueError, ObjectDoesNotExist):
                    pass

        filter_text = filter_text_builder()

        siblings = siblings.filter(d__lt=self.coalesced_published_date())[:5]

        if filter_text:
            if siblings:
                filter_text = mark_safe("You have filtered by " + filter_text)
            else:
                filter_text = mark_safe(
                    "No results for " + filter_text + ", showing latest"
                )

        context.update(
            parent_url=self.get_parent().url,
            filter_text=filter_text,
            siblings=siblings,
            topics=IESGStatementTopic.objects.all()
            .values_list("topic__pk", "topic__title")
            .distinct(),
            query_string=query_string,
            # TODO blog_feed_title=feed_settings.blog_feed_title
        )
        return context

    def serve_preview(self, request, mode_name):
        """This is another hack to overcome the MRO issue we were seeing"""
        return BibliographyMixin.serve_preview(self, request, mode_name)

    class Meta:
        verbose_name = "IESG Statement Page"


IESGStatementPage.content_panels = Page.content_panels + [
    FieldPanel("date_published"),
    FieldPanel("introduction"),
    FieldPanel("body"),
    InlinePanel("topics", label="Topics"),
]

IESGStatementPage.promote_panels = Page.promote_panels + PromoteMixin.panels


class IESGStatementIndexPage(RoutablePageMixin, Page):
    def get_context(self, request):
        context = super().get_context(request)
        context["statements"] = (
            IESGStatementPage.objects.child_of(self)
            .live()
            .annotate(d=Coalesce("date_published", "first_published_at"))
            .order_by("-d")
        )
        return context

    @route(r"^all/$")
    def all_entries(self, request, *args, **kwargs):
        return super().serve(request, *args, **kwargs)

    @route(r"^$")
    def redirect_first(self, request, *args, **kwargs):
        has_filter = False
        for parameter, _ in parameter_functions_map.items():
            if request.GET.get(parameter):
                has_filter = True
                break

        if has_filter:
            statements = (
                IESGStatementPage.objects.child_of(self)
                .live()
                .annotate(d=Coalesce("date_published", "first_published_at"))
                .order_by("-d")
            )
            first_statement_url = statements.first().url
            query_string = "?"

            for parameter, functions in parameter_functions_map.items():
                search_query = request.GET.get(parameter)
                if search_query:
                    try:
                        related_object = functions[0](search_query)
                        statements = functions[1](statements, related_object)
                        query_string += f"{parameter}={search_query}&"
                    except (ValueError, ObjectDoesNotExist):
                        pass
            if statements:
                first_statement_url = statements.first().url
            return redirect(first_statement_url + query_string)
        else:
            return super().serve(request, *args, **kwargs)

    subpage_types = ["iesg_statement.IESGStatementPage"]

    class Meta:
        verbose_name = "IESG Statements Index Page"
