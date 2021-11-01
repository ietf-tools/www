from django.conf import settings

from ietf.blog.models import BlogIndexPage
from ietf.home.models import HomePage
from ietf.utils.models import MenuItem


def home_page():
    return HomePage.objects.filter(depth=2).first()

def menu():
    items = MenuItem.objects.order_by('sort_order').all()
    return items


def global_pages(request):
    return {
        'HOME': home_page(),
        'MENU': menu(),
        'BASE_URL': getattr(settings, 'BASE_URL', ""),
        'DEBUG': getattr(settings, 'DEBUG', ""),
        'FB_APP_ID': getattr(settings, 'FB_APP_ID', ""),
    }
