from datetime import datetime
from functools import partial

from django.db import models
from django.db.models.functions import Coalesce
from django.shortcuts import redirect
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
from ..snippets.models import SecondaryTopic 


def ordered_live_annotated_blogs(sibling=None):
    blogs = BlogPage.objects.live()
    if sibling:
        blogs = blogs.sibling_of(sibling)
    blogs = blogs.annotate(
        d=Coalesce('date_published', 'first_published_at')
    ).order_by('-d')
    return blogs



def filter_pages_by_secondary_topic(pages, secondary_topic):
    return pages.filter(secondary_topics__topic=secondary_topic)


def get_secondary_topic_by_id(id):
    return SecondaryTopic.objects.get(id=id)


def filter_pages_by_date_from(pages, date_from):
    return pages.filter(d__gte=date_from)


def filter_pages_by_date_to(pages, date_to):
    return pages.filter(d__lte=date_to)


def parse_date_search_input(date):
    return datetime.date(datetime.strptime(date, "%d/%m/%Y"))


def build_filter_text(**kwargs):
    if any(kwargs):
        text_fragments = []
        if kwargs.get('secondary_topic'):
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
    'primary_topic': [lambda x: None, lambda x,y : x ],
    'secondary_topic': [get_secondary_topic_by_id,
                        filter_pages_by_secondary_topic],
    'date_from': [parse_date_search_input, filter_pages_by_date_from],
    'date_to': [parse_date_search_input, filter_pages_by_date_to]
}


class BlogPageSecondaryTopic(models.Model):
    """
    A through model from :model:`blog.BlogPage`
    to :model:`snippets.SecondaryTopic`
    """
    page = ParentalKey(
        'blog.BlogPage',
        related_name='secondary_topics'
    )
    topic = models.ForeignKey(
        'snippets.SecondaryTopic',
        related_name='+'
    )

    panels = [
        SnippetChooserPanel('topic')
    ]


class BlogPageAuthor(models.Model):
    """
    A through model from :model:`blog.BlogPage`
    to :model:`datatracker.Person`
    """
    page = ParentalKey(
        'blog.BlogPage',
        related_name='authors'
    )
    author = models.ForeignKey(
        'datatracker.Person',
        on_delete=models.CASCADE,
        related_name='+',
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
        if not siblings:
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
        if not siblings:
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
        return self.__class__.objects.live().sibling_of(self).annotate(
            d=Coalesce('date_published', 'first_published_at')
        ).order_by('-d')

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

        siblings = siblings.filter(d__lt=self.coalesced_published_date())[:5]

        if filter_text:
            if siblings:
                filter_text = mark_safe("You have filtered by " + filter_text)
            else:
                filter_text = mark_safe("No results for " + filter_text + ", showing latest")

        context.update(
            parent_url=self.get_parent().url,
            filter_text = filter_text,
            siblings=siblings,
            secondary_topics=BlogPageSecondaryTopic.objects.all().values_list(
                'topic__pk', 'topic__title'
            ).distinct(),
            query_string=query_string,
            blog_feed_title=feed_settings.blog_feed_title
        )
        return context

    def serve_preview(self, request, mode_name):
        """ This is another hack to overcome the MRO issue we were seeing """
        return BibliographyMixin.serve_preview(self, request, mode_name)

    class Meta:
        verbose_name = "Blog, News, Statement Page"

BlogPage.content_panels = Page.content_panels + [
    InlinePanel('authors', label="Authors"),
    SnippetChooserPanel('author_group'),
    FieldPanel('date_published'),
    FieldPanel('introduction'),
    StreamFieldPanel('body'),
    InlinePanel('secondary_topics', label="Secondary Topics"),
]

BlogPage.promote_panels = Page.promote_panels + PromoteMixin.panels


class BlogIndexPage(RoutablePageMixin, Page):

    def get_context(self, request):
        context = super().get_context(request)
        context['entries'] = BlogPage.objects.child_of(self).live().annotate(
            coalesced_published_date=Coalesce('date_published', 'first_published_at')
        ).order_by('-coalesced_published_date')
        return context

    @route(r'^all/$')
    def all_entries(self, request, *args, **kwargs):
        return super().serve(request,*args,**kwargs)

    @route(r'^$')
    def redirect_first(self, request, *args, **kwargs):
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
            blogs = ordered_live_annotated_blogs()
            first_blog_url = blogs.first().url
            query_string = "?"

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
                first_blog_url = blogs.first().url

            return redirect(first_blog_url + query_string)

    search_fields = []

    subpage_types = ['blog.BlogPage']

    class Meta:
        verbose_name = "Blog, News, Statement Index Page"
