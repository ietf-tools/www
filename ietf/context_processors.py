from operator import itemgetter

from wagtail.models import Site

from ietf.home.models import HomePage, IABHomePage
from ietf.utils.models import MenuItem, SocialMediaSettings


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
    if "iab" in site.hostname:
        return []
    items = (
        MenuItem.objects.order_by("sort_order")
        .all()
        .select_related("page")
        .prefetch_related("sub_menu_items")
    )
    return items


def social_menu(site):
    social = SocialMediaSettings.for_site(site)
    links = [
        {"url": social.linkedin, "icon": "linkedin"},
        {"url": social.twitter, "icon": "twitter"},
        {"url": social.youtube, "icon": "youtube"},
        {"url": social.mastodon, "icon": "mastodon"},
        {"url": social.github, "icon": "github"},
    ]
    return filter(itemgetter("url"), links)


def global_pages(request):
    site = Site.find_for_request(request)
    return {
        "HOME": home_page(site),
        "MENU": menu(site),
        "SECONDARY_MENU": secondary_menu(site),
        "SOCIAL_MENU": social_menu(site),
    }
