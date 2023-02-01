from django.conf import settings
from wagtail.models import Site

from ietf.blog.models import BlogIndexPage
from ietf.home.models import HomePage, IABHomePage
from ietf.utils.models import MenuItem


def home_page(site):
    if "iab" in site.hostname:
        return IABHomePage.objects.filter(depth=2).first()
    return HomePage.objects.filter(depth=2).first()


def children(item):
    return item and item.get_children().live().in_menu()


def menu(site):
    items = children(home_page(site))
    if items:
        for item in items:
            item.subitems = children(item)
    return items


def secondary_menu(site):
    items = (
        MenuItem.objects.order_by("sort_order")
        .all()
        .select_related("page")
        .prefetch_related("sub_menu_items")
    )
    return items


def global_pages(request):
    site = Site.find_for_request(request)
    return {
        "HOME": home_page(site),
        "BLOG_INDEX": BlogIndexPage.objects.first(),
        "MENU": menu(site),
        "SECONDARY_MENU": secondary_menu(site),
        "BASE_URL": getattr(settings, "WAGTAILADMIN_BASE_URL", ""),
        "DEBUG": getattr(settings, "DEBUG", ""),
        "FB_APP_ID": getattr(settings, "FB_APP_ID", ""),
    }
