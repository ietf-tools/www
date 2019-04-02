from wagtail.core.utils import camelcase_to_underscore

from django import template

register = template.Library()


@register.filter
def fieldtype(bound_field):
    return camelcase_to_underscore(bound_field.field.__class__.__name__)


@register.filter
def widgettype(bound_field):
    return camelcase_to_underscore(bound_field.field.widget.__class__.__name__)
