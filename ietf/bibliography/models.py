from bs4 import BeautifulSoup, NavigableString

from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist

from wagtail.core.models import Page

from ietf.utils import OrderedSet


class BibliographyItem(models.Model):
    """
    A single item that is contained in the bibliography of a page.
    """

    # a cache for loaded templates for bibliography items, so we don't have to load them several times for a single bib
    TEMPLATE_CACHE = {}

    ordering = models.PositiveIntegerField(
        help_text="The bibliography items on each referring page are sorted and numbered with this ordering number.",
    )
    page = models.ForeignKey(
        Page,
        related_name='bibliography_items',
        help_text="The page that this item links to.",
        on_delete=models.CASCADE,
    )
    content_key = models.CharField(
        max_length=127,
        help_text='The "key" with which this item was created, eg. "rfc" in [[rfc:3514]].',
    )
    test_key = models.CharField(
        max_length=127,
        help_text='I have no data migration.',
    )
    # Be very wary. The help_text below implies that content_identifier might have an RFC number in it.
    # It does not. Maybe in very early designs that was the plan, but the implementation puts primary
    # keys of the table into this field.
    content_identifier = models.CharField(
        max_length=127,
        help_text='The "value" with which this item was created, eg. "3514" in [[rfc:3514]].',
    )
    content_long_title = models.CharField(
        max_length=127,
        blank=True
    )
    content_title = models.CharField(
        max_length=127,
        help_text='The link title for this item, eg. "RFC 7168" for [[rfc:7168]].',
    )
    content_type = models.ForeignKey(
        ContentType,
        blank=True, null=True,
        on_delete=models.CASCADE,
    )
    object_id = models.PositiveIntegerField(
        blank=True, null=True,
    )
    content_object = GenericForeignKey('content_type', 'object_id')

    def render_title(self):
        if not self.content_object:
            return "(removed)"
        else:
            return self.content_title

    def render_uri(self):
        if not self.content_object:
            return "(removed)"
        else:
            return self.content_object.url

    @property
    def link(self):
        soup = BeautifulSoup("", 'html5lib')
        link = soup.new_tag('a', href="#bibliography" + str(self.ordering))
        link['class'] = "bibliography-reference"
        link['data-ordering'] = str(self.ordering)
        link.insert(0, NavigableString(self.content_title))
        return link

    def render(self, request=None):
        """Render this bibliography item into a displayable item."""

        if not self.content_object:
            return ""

        if self.content_key in BibliographyItem.TEMPLATE_CACHE:
            template = BibliographyItem.TEMPLATE_CACHE[self.content_key]
        else:
            try:
                template = get_template(
                    'bibliography/item_{}.html'.format(self.content_key)
                )
            except TemplateDoesNotExist:
                template = None
            BibliographyItem.TEMPLATE_CACHE[self.content_key] = template

        if template:
            return template.render({
                'object': self.content_object,
                'item': self
            }, request=request)
        else:
            return str(object)

    def __str__(self):
        return "Bibliography Item #{}: {}".format(
            self.ordering, self.content_object
        )


class BibliographyMixin(models.Model):
    def serve_preview(self, request, mode_name):
        """
        This is a temporary hack to get around not having a good way to trigger
        bibliography processing when viewing a page preview.
        """
        for content_field, prepared_content_field in self.CONTENT_FIELD_MAP.items():
            setattr(self, prepared_content_field, getattr(self, content_field))
        return Page.serve_preview(self, request, mode_name)

    def save(self, *args, **kwargs):
        # Don't update prepared content fields if none of the source fields are being updated (e.g. when saving a draft)
        # NB - We have to update all prepared and source fields or none, as there's no way of determining which field a
        #      given BibliographyItem appears in.
        update_fields = kwargs.get('update_fields')
        recreate_bibliography_items = True

        if update_fields is not None:
            source_fields_being_updated = [source_field in update_fields for source_field in self.CONTENT_FIELD_MAP.values()]
            prepared_fields_being_updated = [prepared_field in update_fields for prepared_field in self.CONTENT_FIELD_MAP.keys()]

            if any(source_fields_being_updated) or any(prepared_fields_being_updated):
                if not all(source_fields_being_updated) or not all(prepared_fields_being_updated):
                    raise ValueError('Either all prepared content fields must be updated or none')
            else:
                recreate_bibliography_items = False

        if recreate_bibliography_items:
            self.bibliography_items.all().delete()

            all_content = "".join([
                str(getattr(self, content_field)) or '' for content_field
                in self.CONTENT_FIELD_MAP.keys()
            ])
            all_soup = BeautifulSoup(all_content, 'html.parser')
            subsoups = {
                prepared_content_field: BeautifulSoup(
                    str(getattr(self, content_field)) or '', 'html.parser'
                ) for content_field, prepared_content_field in
                self.CONTENT_FIELD_MAP.items()
            }
            tags = OrderedSet(all_soup.find_all('a', attrs={'data-app': True}))

            for tag in tags:
                app = tag['data-app']
                model = tag['data-linktype']
                obj_id = tag['data-id']

                try:
                    obj = apps.get_model(
                        app_label=app,
                        model_name=model
                    ).objects.get(pk=obj_id)
                    try:
                        long_title = obj.long_title
                    except AttributeError:
                        long_title = ""
                    object_details = {
                        'content_object': obj,
                        'content_long_title': long_title,
                        'content_title': obj.__str__()
                    }
                except ObjectDoesNotExist:
                    object_details = {
                        'content_object': None,
                        'content_long_title': "",
                        'content_title': '(removed)'
                    }
                item = BibliographyItem.objects.create(
                    page=self,
                    ordering=list(tags).index(tag) + 1,
                    content_key=model,
                    content_identifier=obj_id,
                    **object_details
                )
                for soup in subsoups.values():
                    for t in soup.find_all('a', attrs={
                        'data-app': app,
                        'data-linktype': model,
                        'data-id': obj_id
                    }):
                        t.replaceWith(item.link)

            for prepared_content_field, prepared_soup in subsoups.items():
                setattr(self, prepared_content_field, prepared_soup.__unicode__())

        return super(BibliographyMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True
