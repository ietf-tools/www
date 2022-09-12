from django.conf import settings

from ietf.blog.models import BlogIndexPage
from ietf.home.models import HomePage
from ietf.utils.models import MenuItem


def home_page():
    return HomePage.objects.filter(depth=2).first()


def children(item):
    return item and item.get_children().live().in_menu()


def menu():
    items = children(home_page())
    if items:
        for item in items:
            item.subitems = children(item)
    return items


def secondary_menu():
    items = (
        MenuItem.objects.order_by("sort_order")
        .all()
        .select_related("page")
        .prefetch_related("sub_menu_items")
    )
    return items


def global_pages(request):
    return {
        "HOME": home_page(),
        "BLOG_INDEX": BlogIndexPage.objects.first(),
        "MENU": menu(),
        "SECONDARY_MENU": secondary_menu(),
        "BASE_URL": getattr(settings, "WAGTAILADMIN_BASE_URL", ""),
        "DEBUG": getattr(settings, "DEBUG", ""),
        "FB_APP_ID": getattr(settings, "FB_APP_ID", ""),
    }
