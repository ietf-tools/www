from wagtail.core.utils import camelcase_to_underscore

from django import template

register = template.Library()


@register.filter
def fieldtype(bound_field):
    return camelcase_to_underscore(bound_field.field.__class__.__name__)


@register.filter
def widgettype(bound_field):
    return camelcase_to_underscore(bound_field.field.widget.__class__.__name__)

@register.filter(name='add_attr')
def add_attr(bound_field, value):
    attrs = {}
    definition = value.split(',')

    for d in definition:
        if ':' not in d:
            attrs['class'] = d
        else:
            key, val = d.split(':')
            attrs[key] = val

    return bound_field.as_widget(attrs=attrs)
