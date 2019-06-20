from django.db import models
from ietf.blog.models import BlogPageSecondaryTopic

from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import (
    FieldPanel, StreamFieldPanel, InlinePanel, PageChooserPanel
)
from wagtail.search import index
from wagtail.snippets.edit_handlers import (
    SnippetChooserPanel
)

from ..utils.models import PromoteMixin, RelatedLink
from ..utils.blocks import StandardBlock
from ..datatracker.models import (
    WorkingGroup, RFC, InternetDraft
)
from ..snippets.models import (
    PrimaryTopic, SecondaryTopic,
)


class TopicIndexPage(Page, PromoteMixin):
    """
    This page organises topics. Both :model:`topics.PrimaryTopicPage`
    and :model:`topics.SecondaryTopicPage` pages should be placed
    beneath it in the page heirarchy.
    """
    introduction = models.CharField(
        max_length=255,
        help_text="Enter the introduction to display on the page, "
        "you can use only 255 characters."
    )

    search_fields = Page.search_fields + [
        index.SearchField('introduction'),
    ]

    subpage_types = ['topics.PrimaryTopicPage',
                     'topics.SecondaryTopicPage']

    @property
    def primary_topics(self):
        return PrimaryTopicPage.objects.child_of(self)

    @property
    def secondary_topics(self):
        return SecondaryTopicPage.objects.child_of(self)

    class Meta:
        verbose_name = "Topic Page List"

TopicIndexPage.content_panels = Page.content_panels + [
    FieldPanel('introduction'),
]

TopicIndexPage.promote_panels = Page.promote_panels + PromoteMixin.panels


class PrimaryToSecondaryRelationship(models.Model):
    """
    A through model from :model:`topics.PrimaryTopicPage` to
    :model:`topics.SecondaryTopicPage`
    """
    page = ParentalKey('topics.PrimaryTopicPage',
                       related_name='secondary_topics')
    secondary_topic = models.ForeignKey('topics.SecondaryTopicPage',
                                        related_name='primary_topics')

    panels = [
        PageChooserPanel('secondary_topic', 'topics.SecondaryTopicPage')
    ]


class PrimaryTopicPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('topics.PrimaryTopicPage',
                       related_name='related_links')


class PrimaryTopicPage(Page, PromoteMixin):
    """
    This page organises :model:`topics.SecondaryTopicPage` pages through
    :model:`topics.PrimaryToSecondaryRelationship`.

    When this page is saved a :model:`snipppets.PrimaryTopic` snippet
    is created. The snippet is used for organising blog posts.
    """
    introduction = models.CharField(
        blank=True,
        max_length=255,
        help_text="Enter the title to display on the page, you can use only 255 characters."
    )
    key_info = StreamField(StandardBlock(required=False), blank=True)
    in_depth = StreamField(StandardBlock(required=False), blank=True)
    call_to_action = models.ForeignKey(
        'snippets.CallToAction',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Will only be displayed if no mailing list signup is selected."
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

    @property
    def related_topics(self):
        for topic in self.secondary_topics.all():
            yield topic.secondary_topic

    @property
    def feed_text(self):
        return self.search_description or self.introduction

    @property
    def siblings(self):
        return self.get_siblings().live().public().filter(show_in_menus=True).specific()

    def save(self, *args, **kwargs):
        super(PrimaryTopicPage, self).save(*args, **kwargs)
        PrimaryTopic.objects.update_or_create(
            page=self, defaults={'title': self.title}
        )

    class Meta:
        verbose_name = "Topic Page"


PrimaryTopicPage.content_panels = Page.content_panels + [
    FieldPanel('introduction'),
    StreamFieldPanel('key_info'),
    StreamFieldPanel('in_depth'),
    InlinePanel('secondary_topics', label="Secondary Topics"),
    SnippetChooserPanel('call_to_action'),
    SnippetChooserPanel('mailing_list_signup'),
    InlinePanel('related_links', label="Related Links"),
]

PrimaryTopicPage.promote_panels = Page.promote_panels + PromoteMixin.panels


class SecondaryPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('topics.SecondaryTopicPage',
                       related_name='related_links')


class SecondaryTopicPagePerson(models.Model):
    page = ParentalKey('topics.SecondaryTopicPage', related_name='people')
    person = models.ForeignKey('datatracker.Person', related_name='+')

    panels = [
        SnippetChooserPanel('person')
    ]


class SecondaryTopicPage(Page, PromoteMixin):
    """
    Secondary topics correspond to Areas in Datatracker.

    Every :model:`topics.SecondaryTopicPage` page can be linked to
    multiple :model:`topics.PrimaryTopicPage` pages via
    :model:`topics.PrimaryToSecondaryRelationship`.

    When this page is saved a :model:`snipppets.SecondaryTopic` snippet
    is created. The snippet is used for organising blog posts.
    """
    area = models.ForeignKey(
        'datatracker.Area',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    introduction = models.CharField(
        blank=True,
        max_length=255,
        help_text="Enter the introduction to display on the page, "
        "you can use only 255 characters."
    )
    key_info = StreamField(StandardBlock(required=False), blank=True)
    in_depth = StreamField(StandardBlock(required=False), blank=True)
    call_to_action = models.ForeignKey(
        'snippets.CallToAction',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    mailing_list_signup = models.ForeignKey(
        'snippets.MailingListSignup',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + [
        index.SearchField('introduction'),
        index.SearchField('key_info'),
        index.SearchField('in_depth'),
    ]

    @property
    def working_groups(self):
        wgs = WorkingGroup.objects.filter(
            parent=self.area.resource_uri
        )[:6]
        if wgs:
            return (wgs[0:3], wgs[3:6])
        else:
            return None

    @property
    def RFCs(self):
        rfcs = RFC.objects.filter(
            group=self.area.resource_uri
        )[:6]
        if rfcs:
            return (rfcs[0:3], rfcs[3:6])
        else:
            return None

    @property
    def internet_drafts(self):
        drafts = InternetDraft.objects.filter(
            group=self.area.resource_uri
        )[:6]
        if drafts:
            return (drafts[0:3], drafts[3:6])
        else:
            return None

    @property
    def feed_text(self):
        return self.search_description or self.introduction

    @property
    def siblings(self):
        return self.get_siblings().live().public().specific()

    def get_blog_pages(self):
        topic_snippet = SecondaryTopic.objects.filter(page=self).first()
        topic = BlogPageSecondaryTopic.objects.filter(topic=topic_snippet)
        if not topic:
            return []
        return [t.page for t in topic[0:3]]

    def save(self, *args, **kwargs):
        super(SecondaryTopicPage, self).save(*args, **kwargs)
        SecondaryTopic.objects.update_or_create(
            page=self, defaults={'title': self.title}
        )

    class Meta:
        verbose_name = "Area Page"


SecondaryTopicPage.content_panels = Page.content_panels + [
    FieldPanel('area'),
    FieldPanel('introduction'),
    StreamFieldPanel('key_info'),
    StreamFieldPanel('in_depth'),
    InlinePanel('people', label="People"),
    SnippetChooserPanel('call_to_action'),
    SnippetChooserPanel('mailing_list_signup'),
    InlinePanel('related_links', label="Related Links"),
]

SecondaryTopicPage.promote_panels = Page.promote_panels + PromoteMixin.panels
