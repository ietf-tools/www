from datetime import datetime
from functools import partial

from django.db import models
from django.db.models.functions import Coalesce
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.utils import functional
from django.utils.safestring import mark_safe

from modelcluster.fields import ParentalKey

from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.snippets.edit_handlers import (
    SnippetChooserPanel
)
from wagtail.search import index
from wagtail.admin.edit_handlers import (
    StreamFieldPanel, FieldPanel, InlinePanel
)
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from ..bibliography.models import BibliographyMixin
from ..utils.models import FeedSettings, PromoteMixin
from ..utils.blocks import StandardBlock
from ..snippets.models import Topic 


def ordered_live_annotated_blogs(sibling=None):
    blogs = BlogPage.objects.live()
    if sibling:
        blogs = blogs.sibling_of(sibling)
    blogs = blogs.annotate(
        d=Coalesce('date_published', 'first_published_at')
    ).order_by('-d')
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
        if kwargs.get('topic'):
            text_fragments.append(
                '<span>{}</span>'.format(kwargs.get('topic'))
                )
        if kwargs.get('secondary_topic'): # for legacy URI support
            text_fragments.append(
                '<span>{}</span>'.format(kwargs.get('secondary_topic'))
                )
        if kwargs.get('date_from') and kwargs.get('date_to'):
            text_fragments.append(
                'dates between <span>{}</span> &amp; <span>{}</span>'.format(
                    kwargs['date_from'], kwargs['date_to']
                )
            )
        elif kwargs.get('date_from'):
            text_fragments.append('dates after <span>{}</span>'.format(
                kwargs['date_from']
            ))
        elif kwargs.get('date_to'):
            text_fragments.append('dates before <span>{}</span>'.format(
                kwargs['date_to']
            ))
        return ', '.join(text_fragments)
    else:
        return ""


parameter_functions_map = {
    'date_from': [parse_date_search_input, filter_pages_by_date_from],
    'date_to': [parse_date_search_input, filter_pages_by_date_to]
}


class BlogPageTopic(models.Model):
    """
    A through model from :model:`blog.BlogPage`
    to :model:`snippets.Topic`
    """
    page = ParentalKey(
        'blog.BlogPage',
        related_name='topics'
    )
    topic = models.ForeignKey(
        'snippets.Topic',
        related_name='+'
    )

    panels = [
        SnippetChooserPanel('topic')
    ]


class BlogPageAuthor(models.Model):
    """
    A through model from :model:`blog.BlogPage`
    to :model:`snippets.Person`
    """
    page = ParentalKey(
        'blog.BlogPage',
        related_name='authors'
    )
    author = models.ForeignKey(
        'snippets.Person',
        on_delete=models.CASCADE,
        related_name='+',
        null=True, blank=True,
    )
    role = models.ForeignKey(
        'snippets.Role',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Override the person's current role for this blog post."
    )

    panels = [
        SnippetChooserPanel('author'),
        SnippetChooserPanel('role'),
    ]


class BlogPage(Page, BibliographyMixin, PromoteMixin):
    """
    A page for the IETF's news and commentary.
    """
    author_group = models.ForeignKey(
        'snippets.Group',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    date_published = models.DateTimeField(
        null=True, blank=True,
        help_text="Use this field to override the date that the "
        "blog post appears to have been published."
    )
    introduction = models.CharField(
        max_length=511,
        help_text="The page introduction text."
    )
    body = StreamField(StandardBlock())

    search_fields = Page.search_fields + [
        index.SearchField('introduction'),
        index.SearchField('body'),
    ]

    # for bibliography
    prepared_body = models.TextField(
        blank=True, null=True,
        help_text="The prepared body content after bibliography styling has been applied. Auto-generated on each save.",
    )
    CONTENT_FIELD_MAP = {'body': 'prepared_body'}

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
        siblings = self.siblings.exclude(pk=self.pk)
        if not siblings or not self.date:
            return []
        try:
            return [
                sibling for sibling in self.siblings
                if sibling.date < self.date
            ][0]
        except IndexError:
            return siblings[0]

    @property
    def previous(self):
        siblings = list(self.siblings.exclude(pk=self.pk))
        if not siblings or not self.date:
            return []
        try:
            return [
                sibling for sibling in self.siblings
                if sibling.date > self.date
            ][-1]
        except IndexError:
            return siblings[-1]

    def coalesced_published_date(self):
        return self.date_published or self.first_published_at

    @property
    def feed_text(self):
        return self.search_description or self.introduction

    @functional.cached_property
    def siblings(self):
        qs = self.__class__.objects.live().sibling_of(self).annotate(
            d=Coalesce('date_published', 'first_published_at')
        ).order_by('-d')
        if self.filter_topic:
            qs = qs.filter(topics__topic=self.filter_topic)
        return qs

    def get_context(self, request, *args, **kwargs):
        context = super(BlogPage, self).get_context(request, *args, **kwargs)
        siblings = self.siblings
        query_string = "?"
        filter_text_builder = build_filter_text
        feed_settings = FeedSettings.for_site(request.site)

        # This is mostly duplicted in BlogIndexPage
        for parameter, functions in parameter_functions_map.items():
            search_query = request.GET.get(parameter)
            if search_query:
                try:
                    related_object = functions[0](search_query)
                    siblings = functions[1](siblings, related_object)
                    query_string += "%s=%s&" % (parameter, search_query)
                    filter_text_builder = partial(filter_text_builder,
                                                  **{parameter: related_object.__str__()})
                except (ValueError, ObjectDoesNotExist):
                    pass

        filter_text = filter_text_builder()

        if self.filter_topic:
            if filter_text:
                filter_text = ','.join([self.filter_topic.title, filter_text])
            else:
                filter_text = self.filter_topic.title

        if self.coalesced_published_date():
            siblings = siblings.filter(d__lt=self.coalesced_published_date() or datetime.now())[:5]
        else:
            siblings = siblings.none()

        if filter_text:
            if siblings:
                filter_text = mark_safe("You have filtered by " + filter_text)
            else:
                filter_text = mark_safe("No results for " + filter_text + ", showing latest")

        context.update(
            parent_url=self.get_parent().url,
            filter_text = filter_text,
            filter_topic = self.filter_topic,
            siblings=siblings,
            topics=BlogPageTopic.objects.all().values_list(
                'topic__pk', 'topic__title'
            ).distinct(),
            query_string=query_string,
            blog_feed_title=feed_settings.blog_feed_title
        )
        return context

    def serve(self, request, *args, **kwargs):
        topic_id = request.GET.get('topic')
        if not topic_id:
            topic_id = request.GET.get('secondary_topic') # For legacy URI support
        if topic_id:
            try:
                topic_id = int(topic_id)
            except ValueError:
                raise Http404
            filter_topic = get_object_or_404(Topic,id=topic_id)
            query_string_segments=[]
            for parameter, function in parameter_functions_map.items():
                search_query = request.GET.get(parameter)
                if search_query:
                    query_string_segments.append('%s=%s' % (parameter, search_query))
            query_string = '&'.join(query_string_segments)
            target_url = self.get_parent().specific.reverse_subpage('redirect_first',args=(filter_topic.slug,))
            if query_string:
                target_url = target_url + '?' + query_string
            return redirect(target_url)
        else:
            return super().serve(request, *args, **kwargs)

    def serve_preview(self, request, mode_name):
        """ This is another hack to overcome the MRO issue we were seeing """
        return BibliographyMixin.serve_preview(self, request, mode_name)

    class Meta:
        verbose_name = "Blog Page"

BlogPage.content_panels = Page.content_panels + [
    InlinePanel('authors', label="Authors"),
    SnippetChooserPanel('author_group'),
    FieldPanel('date_published'),
    FieldPanel('introduction'),
    StreamFieldPanel('body'),
    InlinePanel('topics', label="Topics"),
]

BlogPage.promote_panels = Page.promote_panels + PromoteMixin.panels


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
            coalesced_published_date=Coalesce('date_published', 'first_published_at')
        ).order_by('-coalesced_published_date')
        context['entries'] = entry_qs
        context['topics'] = sorted(set([p.topic for p in BlogPageTopic.objects.all()]),key=lambda x:x.title)
        return context

    @route(r'^all/$')
    def all_entries(self, request, *args, **kwargs):
        return super().serve(request, *args, **kwargs)

    @route(r'^([-\w]+)/all/$')
    def filtered_entries(self, request, slug, *args, **kwargs):
        self.filter_topic = get_object_or_404(Topic,slug=slug)
        return super().serve(request, *args, **kwargs)

    @route(r'^([-\w]+)/$')
    @route(r'^$')
    def redirect_first(self, request, slug=None, *args, **kwargs):
        # IESG statements were moved under the IESG about/groups page. Queries to the
        # base /blog/ page that used a query string to filter for IESG statements can't
        # be redirected through ordinary redirection, so we're doing it here.
        if request.GET.get('primary_topic')=='7':
            query_string = ''
            topic = request.GET.get('secondary_topic')
            if topic:
                query_string = query_string + 'topic=' + topic
            date_from = request.GET.get('date_from')
            if date_from:
                separator = '&' if query_string else ''
                query_string = query_string + separator + 'date_from=' + date_from
            date_to = request.GET.get('date_to')
            if date_to:
                separator = '&' if query_string else ''
                query_string = query_string + separator + 'date_to' + date_to
            target_url = '/about/groups/iesg/statements'
            if query_string:
                target_url = target_url + '?' + query_string
            return redirect(target_url)
        else:
            if slug:
                self.filter_topic = Topic.objects.filter(slug=slug).first()
                if not self.filter_topic:
                    blog_page = get_object_or_404(BlogPage,slug=slug)
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


    search_fields = []

    subpage_types = ['blog.BlogPage']

    class Meta:
        verbose_name = "Blog Index Page"
