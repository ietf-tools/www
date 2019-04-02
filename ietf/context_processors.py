from django.conf import settings
from django.db.models.functions import Coalesce

from ietf.blog.models import BlogIndexPage
from ietf.home.models import HomePage


def home_page():
    return HomePage.objects.filter(depth=2).first()


def children(item):
    return item.get_children().live().in_menu()


def menu():
    items = children(home_page())
    for item in items:
        item.subitems = children(item)
    return items


def global_pages(request):
    return {
        'HOME': home_page(),
        'BLOG_INDEX': BlogIndexPage.objects.first(),
        'MENU': menu(),
        'BASE_URL': getattr(settings, 'BASE_URL', ""),
        'DEBUG': getattr(settings, 'DEBUG', ""),
        'FB_APP_ID': getattr(settings, 'FB_APP_ID', ""),
    }
