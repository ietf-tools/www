from future.standard_library import install_aliases
install_aliases()

import re
import time
from urllib.parse import unquote

import requests

from requests import exceptions

from django.db import models
from django.utils.html import strip_tags
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from modelcluster.queryset import FakeQuerySet

from wagtail.search import index
from wagtail.snippets.models import register_snippet

from ..snippets.models import Group

DATATRACKER_URI = "https://datatracker.ietf.org"
DATATRACKER_TIMEOUT = 30
DATATRACKER_ITEMS_PER_PAGE = 50


class DatatrackerMeta(models.Model):
    """
    Contains metadata for Datatracker-related models
    """
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    last_page_seen = models.CharField(max_length=511, blank=True)
    last_updated = models.DateTimeField(null=True, blank=True)

    @property
    def local_count(self):
        return self.content_type.model_class().objects.filter(active=True).count()

    @property
    def remote_count(self):
        params = {'format': 'json'}
        params.update(self.content_type.model_class().ARGS)
        return requests.get(
            DATATRACKER_URI + self.content_type.model_class().PATH, params=params, timeout=DATATRACKER_TIMEOUT
        ).json()['meta']['total_count']


class DatatrackerMixin(object):
    """
    Methods to do a complete refresh from the datatracker api
    """
    @staticmethod
    def datatracker(path, meta=None, **kwargs):
        """
        A generator that requests data from Datatracker and handles paging.
        """
        params = {'format': 'json', 'limit': DATATRACKER_ITEMS_PER_PAGE}
        params.update(kwargs)
        results = requests.get(DATATRACKER_URI + path, params=params, timeout=DATATRACKER_TIMEOUT).json()
        for result in results['objects']:
            yield result
        next = results['meta']['next']
        last_page_seen = next
        while next:
            try:
                results = requests.get(
                    DATATRACKER_URI + next, timeout=DATATRACKER_TIMEOUT
                ).json()
            except exceptions.ReadTimeout:
                # Try to avoid hitting Datatracker too hard
                time.sleep(5)
                results = requests.get(
                    DATATRACKER_URI + next, timeout=DATATRACKER_TIMEOUT
                ).json()
            except ValueError as e:
                print("invalid response from datatracker: %s" % e)
                break
            try:
                for result in results['objects']:
                    yield result
            except KeyError:
                print("No 'objects' property on page %s" % next)
                break
            last_page_seen = next
            next = results['meta']['next']
        if meta:
            if last_page_seen:
                meta.last_page_seen = last_page_seen
            else:
                meta.last_page_seen = ""
            meta.save()

    @classmethod
    def fetch(cls, meta=None):
        return cls.datatracker(cls.PATH, meta=meta, **cls.ARGS)

    @classmethod
    def fetch_and_update(cls):
        # Update metadata
        meta, created = DatatrackerMeta.objects.get_or_create(
            content_type=ContentType.objects.get_for_model(cls)
        )
        meta.last_updated = timezone.now()

        active_items = []
        for item in cls.fetch(meta=meta):
            active_items.append(item[cls.IDENTIFIER])
            defaults = {'active': True}
            for field in cls.FIELDS:
                if item[field]:
                    defaults[field] = strip_tags(item[field])
                else:
                    defaults[field] = ""
            args = {'defaults': defaults}
            args[cls.IDENTIFIER] = item[cls.IDENTIFIER]
            try:
                item_obj, created = cls.objects.update_or_create(**args)
            except Exception as e:
                print("could not execute import, update error")
                import traceback
                traceback.print_exc()
                # we will not raise this exception since it only applies to a single items; so it will be skipped
        # If it's in the database but not returned by the
        # API it's inactive and shouldn't be displayed
        try:
            cls.objects.exclude(
                **{cls.IDENTIFIER + '__in': active_items}
            ).update(active=False)
        except Exception as e:
            print("could not disable inactive items, update error")
            import traceback
            traceback.print_exc()
            raise

        return len(active_items)


@register_snippet
class Area(DatatrackerMixin, models.Model, index.Indexed):
    PATH = '/api/v1/group/group/'
    ARGS = {'type': 'area'}
    FIELDS = [
        'name',
        'resource_uri',
        'list_email',
        'list_subscribe',
        'acronym'
    ]
    IDENTIFIER = 'id'

    active = models.BooleanField(default=False)
    name = models.CharField(max_length=511)
    resource_uri = models.CharField(max_length=511)
    list_email = models.EmailField(blank=True)
    list_subscribe = models.EmailField(blank=True)
    acronym = models.CharField(max_length=511, blank=True)

    search_fields = [
        index.SearchField('name', partial_match=True, boost=10),
        index.SearchField('acronym'),
    ]

    @property
    def url(self):
        return DATATRACKER_URI + "/wg/#" + self.acronym

    @staticmethod
    def extract_acronym(url):
        return url.split(DATATRACKER_URI + "/wg/#")[1]

    def working_groups(self):
        return WorkingGroup.objects.filter(parent=self.resource_uri, active=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Area"


@register_snippet
class WorkingGroup(DatatrackerMixin, models.Model, index.Indexed):
    PATH = '/api/v1/group/group/'
    ARGS = {'state': 'active', 'type': 'wg'}
    FIELDS = [
        'name',
        'parent',
        'description',
        'acronym',
        'comments',
        'charter',
        'resource_uri',
        'list_email',
        'list_subscribe'
    ]
    IDENTIFIER = 'id'

    active = models.BooleanField(default=False)
    name = models.CharField(max_length=511)
    resource_uri = models.CharField(max_length=511)
    parent = models.CharField(max_length=511, blank=True)
    acronym = models.CharField(max_length=511, blank=True)
    description = models.CharField(max_length=4096, blank=True)
    comments = models.CharField(max_length=4096, blank=True)
    charter = models.CharField(max_length=511, blank=True)
    list_email = models.EmailField(blank=True)
    list_subscribe = models.EmailField(blank=True)

    search_fields = [
        index.SearchField('name', partial_match=True, boost=10),
        index.SearchField('acronym'),
        index.SearchField('description'),
    ]

    @property
    def url(self):
        return DATATRACKER_URI + "/wg/" + self.acronym

    @property
    def charter_url(self):
        return self.url + "/charter/"

    @property
    def group_snippets(self):
        return Group.objects.filter(email=self.list_email, active=True)

    def get_charter_acronym(self):
        if self.charter:
            return self.charter.split('/')[-2]
        else:
            return ""

    def get_area(self):
        return Area.objects.filter(resource_uri=self.parent, active=True).first()

    @staticmethod
    def extract_acronym(url):
        return url.split(DATATRACKER_URI + "/wg/")[1]

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Working Group"


@register_snippet
class RFC(DatatrackerMixin, models.Model, index.Indexed):
    PATH = '/api/v1/doc/document/'
    ARGS = {'states__slug': 'rfc'}
    FIELDS = [
        'name',
        'resource_uri',
        'title',
        'rfc',
        # 'authors',
        'abstract',
        'group',
        'time'
    ]
    IDENTIFIER = 'rfc'

    active = models.BooleanField(default=False)
    name = models.CharField(max_length=511)
    resource_uri = models.CharField(max_length=511)
    title = models.TextField(blank=True)
    rfc = models.CharField(max_length=511, unique=True)
    authors = models.TextField(blank=True)
    abstract = models.TextField(blank=True)
    group = models.CharField(max_length=511)
    time = models.CharField(max_length=511, blank=True)

    search_fields = [
        index.SearchField('title', partial_match=True, boost=10),
        index.SearchField('rfc', boost=10),
        index.SearchField('authors'),
        index.SearchField('abstract'),
    ]

    def __str__(self):
        return "RFC {}".format(self.rfc)

    @property
    def long_title(self):
        return self.title

    @staticmethod
    def extract_rfc_number(url):
        return url.split(DATATRACKER_URI + "/doc/rfc")[1]

    @property
    def working_group(self):
        return WorkingGroup.objects.filter(
            resource_uri=self.group,
            active=True
        ).first()

    @property
    def url(self):
        return DATATRACKER_URI + "/doc/rfc" + self.rfc

    @property
    def author_emails(self):
        return [
            unquote(author) for author in re.findall(
                r"/api/v1/person/email/([^/]+)/", self.authors
            )
        ]

    @property
    def author_snippets(self):
        people_uris = Email.objects.filter(
            address__in=self.author_emails,
            active=True
        ).values_list('person')
        return Person.objects.filter(resource_uri__in=people_uris, active=True)

    @property
    def author_names(self):
        return [author.name for author in self.author_snippets]

    class Meta:
        ordering = ['title']
        verbose_name = "RFC"


@register_snippet
class InternetDraft(DatatrackerMixin, models.Model, index.Indexed):
    PATH = '/api/v1/doc/document/'
    ARGS = {'states__type__slug': 'draft', 'states__slug': 'active'}
    FIELDS = [
        'name',
        'resource_uri',
        'title',
        # 'authors',
        'abstract',
        'group'
    ]
    IDENTIFIER = 'name'

    active = models.BooleanField(default=False)
    name = models.CharField(max_length=511, unique=True)
    resource_uri = models.CharField(max_length=511)
    title = models.TextField(blank=True)
    authors = models.TextField(blank=True)
    abstract = models.TextField(blank=True)
    group = models.CharField(max_length=511)

    rearch_fields = [
        index.SearchField('title', partial_match=True, boost=10),
        index.SearchField('authors'),
        index.SearchField('abstract'),
        index.SearchField('name'),
    ]

    def __str__(self):
        return self.title

    @property
    def working_group(self):
        return WorkingGroup.objects.filter(
            resource_uri=self.group,
            active=True
        ).first()

    @property
    def url(self):
        return DATATRACKER_URI + "/doc/" + self.name

    @staticmethod
    def extract_name(url):
        return url.split(DATATRACKER_URI + "/doc/")[1]

    class Meta:
        ordering = ['title']
        verbose_name = "Internet Draft"


@register_snippet
class Charter(DatatrackerMixin, models.Model, index.Indexed):
    PATH = '/api/v1/doc/document/'
    ARGS = {'type': 'charter'}
    FIELDS = [
        'name',
        'resource_uri',
        'title',
        # 'authors',
        'abstract',
        'group'
    ]
    IDENTIFIER = 'name'

    active = models.BooleanField(default=False)
    name = models.CharField(max_length=511, unique=True)
    resource_uri = models.CharField(max_length=511)
    title = models.TextField(blank=True)
    authors = models.TextField(blank=True)
    abstract = models.TextField(blank=True)
    group = models.CharField(max_length=511)

    search_fields = [
        index.SearchField('title', partial_match=True, boost=10),
        index.SearchField('authors'),
        index.SearchField('abstract'),
    ]

    def __str__(self):
        return self.title

    @property
    def working_group(self):
        return WorkingGroup.objects.filter(resource_uri=self.group, active=True).first()

    @property
    def url(self):
        if self.working_group:
            return self.working_group.charter_url
        else:
            return ""

    @property
    def area(self):
        return Area.objects.filter(resource_uri=self.group, active=True).first()

    @staticmethod
    def extract_group(url):
        return WorkingGroup.objects.filter(
            acronym=WorkingGroup.extract_acronym(
                url.split(DATATRACKER_URI + "/charter/")[0]
            ),
            active=True
        ).first()

    class Meta:
        ordering = ['title']
        verbose_name = "Charter"


@register_snippet
class RoleName(DatatrackerMixin, models.Model, index.Indexed):
    PATH = '/api/v1/name/rolename/'
    ARGS = {}
    FIELDS = [
        'name',
        'resource_uri',
        'slug',
    ]
    IDENTIFIER = 'slug'

    active = models.BooleanField(default=False)
    name = models.CharField(max_length=511)
    resource_uri = models.CharField(max_length=511)
    slug = models.CharField(max_length=511, unique=True)

    class Meta:
        verbose_name = "Role Name"


@register_snippet
class Role(DatatrackerMixin, models.Model, index.Indexed):
    PATH = '/api/v1/group/role/'
    ARGS = {}
    FIELDS = [
        'email',
        'group',
        'person',
        'name',
        'resource_uri',
    ]
    IDENTIFIER = 'id'

    active = models.BooleanField(default=False)
    email = models.CharField(max_length=511)
    name = models.CharField(max_length=511)
    person = models.CharField(max_length=511)
    group = models.CharField(max_length=511)
    resource_uri = models.CharField(max_length=511)

    class Meta:
        verbose_name = "Role"


@register_snippet
class Email(DatatrackerMixin, models.Model, index.Indexed):
    PATH = '/api/v1/person/email/'
    ARGS = {'active': True}
    FIELDS = [
        'address',
        'person',
        'resource_uri',
    ]
    IDENTIFIER = 'resource_uri'

    active = models.BooleanField(default=False)
    resource_uri = models.CharField(max_length=511, unique=True)
    address = models.CharField(max_length=511)
    person = models.CharField(max_length=511)

    class Meta:
        verbose_name = "Email"


@register_snippet
class Person(DatatrackerMixin, models.Model, index.Indexed):
    PATH = '/api/v1/person/person/'
    ARGS = {}
    FIELDS = [
        'name',
        'resource_uri',
        'biography',
        'photo',
        'photo_thumb',
    ]
    IDENTIFIER = 'id'

    active = models.BooleanField(default=False)
    name = models.CharField(max_length=511)
    resource_uri = models.CharField(max_length=511)
    biography = models.TextField(blank=True)
    resource_uri = models.CharField(max_length=511)
    photo = models.CharField(max_length=511)
    photo_thumb = models.CharField(max_length=511)

    search_fields = [
        index.SearchField('name', partial_match=True, boost=10),
        index.SearchField('biography', partial_match=True, boost=10),
    ]

    @property
    def role(self):
        try:
            # A person can have multiple roles, but we only have space to
            # display one
            role = Role.objects.filter(person=self.resource_uri).first()
            return RoleName.objects.get(resource_uri=role.name, active=True).name
        except (AttributeError, RoleName.DoesNotExist):
            return ""

    @property
    def email(self):
        try:
            # A person can have multiple emails, but we only have space to
            # display one
            return Email.objects.filter(person=self.resource_uri, active=True).first().address
        except AttributeError:
            return ""

    def __str__(self):
        # FIXME this is here for compatibility between Python versions 2 and 3
        # remove once production is on Python 3
        try:
            return unicode(self).encode('utf-8')
        except NameError:
            return self.name

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Person"
        verbose_name_plural = "People"

