from wagtail.core import hooks
from django.utils.html import format_html
from django.conf import settings


@hooks.register('insert_editor_css')
def editor_css():
    return format_html('<link rel="stylesheet" href="' \
    + settings.STATIC_URL \
    + 'utils/css/page_editor.css">')