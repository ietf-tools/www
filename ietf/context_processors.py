from operator import itemgetter

from wagtail.models import Site

from ietf.home.models import HomePage, IABHomePage
from ietf.utils.context_processors import get_footer, get_main_menu
from ietf.utils.models import SecondaryMenuItem, SocialMediaSettings


def home_page(site):
    if "iab" in site.hostname:
        return IABHomePage.objects.filter(depth=2).first()
    return HomePage.objects.filter(depth=2).first()


def secondary_menu(site):
    if "iab" in site.hostname:
        return []
    items = (
        SecondaryMenuItem.objects.order_by("sort_order")
        .all()
        .select_related("page")
        .prefetch_related("sub_menu_items")
    )
    return items


def social_menu(site):
    social = SocialMediaSettings.for_site(site)
    links = [
        {"url": social.linkedin, "icon": "linkedin", "title": "LinkedIn"},
        {"url": social.twitter, "icon": "twitter", "title": "Twitter"},
        {"url": social.youtube, "icon": "youtube", "title": "YouTube"},
        {"url": social.mastodon, "icon": "mastodon", "title": "Mastodon"},
        {"url": social.github, "icon": "github", "title": "GitHub"},
    ]
    return filter(itemgetter("url"), links)


def global_pages(request):
    site = Site.find_for_request(request)
    # XXX Return lazy values. This makes a big difference when a page renders
    # multiple templates, e.g. when the wagtail userbar is displayed.
    return {
        "HOME": lambda: home_page(site),
        "MENU": lambda: get_main_menu(site),
        "SECONDARY_MENU": lambda: secondary_menu(site),
        "SOCIAL_MENU": lambda: social_menu(site),
        "FOOTER": lambda: get_footer(),
    }
