from dataclasses import dataclass
from datetime import datetime
from functools import partial

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.functions import Coalesce
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import functional
from django.utils.safestring import mark_safe
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.fields import StreamField
from wagtail.models import Page, Site
from wagtail.search import index

from ..bibliography.models import BibliographyMixin
from ..snippets.models import Person, Topic
from ..utils.blocks import StandardBlock
from ..utils.models import FeedSettings, PromoteMixin


def ordered_live_annotated_blogs(sibling=None):
    blogs = BlogPage.objects.live().prefetch_related("authors")
    if sibling:
        blogs = blogs.sibling_of(sibling)
    blogs = blogs.annotate(d=Coalesce("date_published", "first_published_at")).order_by(
        "-d"
    )
    return blogs


def filter_pages_by_date_from(pages, date_from):
    return pages.filter(d__gte=date_from)


def filter_pages_by_date_to(pages, date_to):
    return pages.filter(d__lte=date_to)


def parse_date_search_input(date):
    return datetime.date(datetime.strptime(date, "%d/%m/%Y"))


def build_filter_text(**kwargs):
    if any(kwargs):
        text_fragments = []
        if kwargs.get("topic"):
            text_fragments.append("<span>{}</span>".format(kwargs.get("topic")))
        if kwargs.get("secondary_topic"):  # for legacy URI support
            text_fragments.append(
                "<span>{}</span>".format(kwargs.get("secondary_topic"))
            )
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
    "date_from": [parse_date_search_input, filter_pages_by_date_from],
    "date_to": [parse_date_search_input, filter_pages_by_date_to],
}


class BlogPageTopic(models.Model):
    """
    A through model from :model:`blog.BlogPage`
    to :model:`snippets.Topic`
    """

    page = ParentalKey("blog.BlogPage", related_name="topics")
    topic = models.ForeignKey(
        "snippets.Topic",
        related_name="+",
        on_delete=models.CASCADE,
    )

    panels = [FieldPanel("topic")]


class BlogPageAuthor(models.Model):
    """
    A through model from :model:`blog.BlogPage`
    to :model:`snippets.Person`
    """

    page = ParentalKey("blog.BlogPage", related_name="authors")
    author = models.ForeignKey(
        "snippets.Person",
        on_delete=models.CASCADE,
        related_name="+",
    )
    role = models.ForeignKey(
        "snippets.Role",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Override the person's current role for this blog post.",
    )

    panels = [
        FieldPanel("author"),
        FieldPanel("role"),
    ]


class BlogPage(Page, BibliographyMixin, PromoteMixin):
    """
    A page for the IETF's news and commentary.
    """

    author_group = models.ForeignKey(
        "snippets.Group",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filter_topic = None

    @property
    def first_author(self):
        try:
            return self.authors.first().author
        except AttributeError:
            return self.authors.none()

    @property
    def date(self):
        return self.date_published or self.first_published_at

    @property
    def next(self):
        if not self.date:
            return None
        after = sorted(
            [p for p in self.siblings if p.date > self.date], key=lambda o: o.date
        )
        return after and after[0] or None

    @property
    def previous(self):
        if not self.date:
            return None
        before = sorted(
            [p for p in self.siblings if p.date < self.date],
            key=lambda o: o.date,
            reverse=True,
        )
        return before and before[0] or None

    def coalesced_published_date(self):
        return self.date_published or self.first_published_at

    @property
    def feed_text(self):
        return self.search_description or self.introduction

    @functional.cached_property
    def siblings(self):
        """Published siblings that match filter_topic, most recent first"""
        qs = (
            self.__class__.objects.live()
            .sibling_of(self)
            .exclude(pk=self.pk)
            .annotate(d=Coalesce("date_published", "first_published_at"))
            .order_by("-d")
        )
        if self.filter_topic:
            qs = qs.filter(topics__topic=self.filter_topic)
        return qs

    def get_blog_index_page(self):
        for parent in self.get_ancestors().specific():
            if isinstance(parent, BlogIndexPage):
                return parent
        else:
            raise ValueError("Cannot find parent BlogIndexPage")

    def get_authors(self):
        index_page = self.get_blog_index_page()

        return [
            {
                "name": author.author.name,
                "url": index_page.url + index_page.reverse_subpage(
                    "index_by_author", kwargs={"slug": author.author.slug}
                ),
                "role": author.role,
            }
            for author in self.authors.all()
        ]

    def get_context(self, request, *args, **kwargs):
        context = super(BlogPage, self).get_context(request, *args, **kwargs)
        siblings = self.siblings
        max_siblings_to_show = 5
        query_string = "?"
        filter_text_builder = build_filter_text
        feed_settings = FeedSettings.for_site(Site.find_for_request(request))

        # This is mostly duplicted in BlogIndexPage
        for parameter, functions in parameter_functions_map.items():
            search_query = request.GET.get(parameter)
            if search_query:
                try:
                    related_object = functions[0](search_query)
                    siblings = functions[1](siblings, related_object)
                    query_string += "%s=%s&" % (parameter, search_query)
                    filter_text_builder = partial(
                        filter_text_builder, **{parameter: related_object.__str__()}
                    )
                except (ValueError, ObjectDoesNotExist):
                    pass

        filter_text = filter_text_builder()

        if self.filter_topic:
            if filter_text:
                filter_text = ",".join([self.filter_topic.title, filter_text])
            else:
                filter_text = self.filter_topic.title

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
            filter_topic=self.filter_topic,
            siblings=siblings[:max_siblings_to_show],
            topics=BlogPageTopic.objects.all()
            .values_list("topic__pk", "topic__title")
            .distinct(),
            query_string=query_string,
            blog_feed_title=feed_settings.blog_feed_title,
        )
        return context

    def serve(self, request, *args, **kwargs):
        topic_id = request.GET.get("topic")
        if not topic_id:
            topic_id = request.GET.get("secondary_topic")  # For legacy URI support
        if topic_id:
            try:
                topic_id = int(topic_id)
            except ValueError:
                raise Http404
            filter_topic = get_object_or_404(Topic, id=topic_id)
            query_string_segments = []
            for parameter, function in parameter_functions_map.items():
                search_query = request.GET.get(parameter)
                if search_query:
                    query_string_segments.append("%s=%s" % (parameter, search_query))
            query_string = "&".join(query_string_segments)
            target_url = self.get_parent().specific.reverse_subpage(
                "redirect_first", args=(filter_topic.slug,)
            )
            if query_string:
                target_url = target_url + "?" + query_string
            return redirect(target_url)
        else:
            return super().serve(request, *args, **kwargs)

    def serve_preview(self, request, mode_name):
        """This is another hack to overcome the MRO issue we were seeing"""
        return BibliographyMixin.serve_preview(self, request, mode_name)

    class Meta:
        verbose_name = "Blog Page"


BlogPage.content_panels = Page.content_panels + [
    InlinePanel("authors", label="Authors"),
    FieldPanel("author_group"),
    FieldPanel("date_published"),
    FieldPanel("introduction"),
    FieldPanel("body"),
    InlinePanel("topics", label="Topics"),
]

BlogPage.promote_panels = Page.promote_panels + PromoteMixin.panels


@dataclass
class BlogIndexByAuthorPage:
    """
    An ephemeral Page-like class to render the author listing page. It allows
    us to use the existing templates for e.g. page title and breadcrumbs.
    """

    person: Person
    parent: "BlogIndexPage"

    @property
    def title(self):
        return f"Articles by {self.person.name}"

    def get_ancestors(self):
        return self.parent.get_ancestors(inclusive=True)

    def get_entries_queryset(self):
        qs = BlogPage.objects.child_of(self.parent).filter(authors__author=self.person).live()
        qs = qs.annotate(
            coalesced_published_date=Coalesce("date_published", "first_published_at")
        ).order_by("-coalesced_published_date")
        return qs

    def serve(self, request):
        context = {
            "entries": self.get_entries_queryset(),
            "self": self,
        }
        return render(request, "blog/blog_index_by_author.html", context)

    def feed(self, request):
        from .feeds import AuthorBlogFeed

        return AuthorBlogFeed(self.person, self.get_entries_queryset())(request)


class BlogIndexPage(RoutablePageMixin, Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filter_topic = None

    def get_context(self, request):
        context = super().get_context(request)
        entry_qs = BlogPage.objects.child_of(self).live()
        if self.filter_topic:
            entry_qs = entry_qs.filter(topics__topic=self.filter_topic)
        entry_qs = entry_qs.annotate(
            coalesced_published_date=Coalesce("date_published", "first_published_at")
        ).order_by("-coalesced_published_date")
        context["entries"] = entry_qs
        context["topics"] = sorted(
            set([p.topic for p in BlogPageTopic.objects.all()]), key=lambda x: x.title
        )
        return context

    @route(r"^all/$")
    def all_entries(self, request, *args, **kwargs):
        return super().serve(request, *args, **kwargs)

    @route(r"^author/(?P<slug>[^/]+)/$", name="index_by_author")
    def index_by_author(self, request, slug):
        person = get_object_or_404(Person, slug=slug)
        return BlogIndexByAuthorPage(person=person, parent=self).serve(request)

    @route(r"^author/(?P<slug>[^/]+)/feed/$", name="feed_by_author")
    def feed_by_author(self, request, slug):
        person = get_object_or_404(Person, slug=slug)
        return BlogIndexByAuthorPage(person=person, parent=self).feed(request)

    @route(r"^(?P<topic>.+)/feed/$", name="blog_feed_with_topic")
    def feed_with_topic(self, request, topic):
        from .feeds import TopicBlogFeed

        return TopicBlogFeed()(request, topic=topic)

    @route(r"^([-\w]+)/all/$")
    def filtered_entries(self, request, slug, *args, **kwargs):
        self.filter_topic = get_object_or_404(Topic, slug=slug)
        return super().serve(request, *args, **kwargs)

    @route(r"^([-\w]+)/$")
    @route(r"^$")
    def redirect_first(self, request, slug=None, *args, **kwargs):
        # IESG statements were moved under the IESG about/groups page. Queries to the
        # base /blog/ page that used a query string to filter for IESG statements can't
        # be redirected through ordinary redirection, so we're doing it here.
        if request.GET.get("primary_topic") == "7":
            query_string = ""
            topic = request.GET.get("secondary_topic")
            if topic:
                query_string = query_string + "topic=" + topic
            date_from = request.GET.get("date_from")
            if date_from:
                separator = "&" if query_string else ""
                query_string = query_string + separator + "date_from=" + date_from
            date_to = request.GET.get("date_to")
            if date_to:
                separator = "&" if query_string else ""
                query_string = query_string + separator + "date_to" + date_to
            target_url = "/about/groups/iesg/statements"
            if query_string:
                target_url = target_url + "?" + query_string
            return redirect(target_url)
        else:
            if slug:
                self.filter_topic = Topic.objects.filter(slug=slug).first()
                if not self.filter_topic:
                    blog_page = get_object_or_404(
                        BlogPage.objects.prefetch_related("authors"), slug=slug
                    )
                    return blog_page.serve(request, *args, **kwargs)

            blogs = ordered_live_annotated_blogs()

            first_blog = blogs.first()
            query_string = "?"

            if self.filter_topic:
                blogs = blogs.filter(topics__topic=self.filter_topic)

            # This is duplicated in BlogPage
            for parameter, functions in parameter_functions_map.items():
                search_query = request.GET.get(parameter)
                if search_query:
                    try:
                        related_object = functions[0](search_query)
                        blogs = functions[1](blogs, related_object)
                        query_string += "%s=%s&" % (parameter, search_query)
                    except (ValueError, ObjectDoesNotExist):
                        pass

            if blogs:
                first_blog = blogs.first()

            # If blogs is empty above, should we really be serving something unrelated to the filters?
            first_blog.filter_topic = self.filter_topic

            return first_blog.serve(request, *args, **kwargs)

    search_fields = Page.search_fields + []

    subpage_types = ["blog.BlogPage"]

    class Meta:
        verbose_name = "Blog Index Page"
