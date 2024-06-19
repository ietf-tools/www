from django import template

register = template.Library()


@register.simple_tag
def has_tabs(key_info, in_depth):
    return bool(key_info and in_depth)
