from urllib.parse import quote

from django.template import Library
from wagtail.models import Site

from ..models import PromoteMixin, SocialMediaSettings

register = Library()


@register.simple_tag(takes_context=False)
def social_text(page, site, encode=False):
    text = ""

    if isinstance(page, PromoteMixin):
        text = page.get_social_text()

    if not text:
        text = SocialMediaSettings.for_site(site).default_sharing_text

    if encode:
        text = quote(text)

    return text


@register.simple_tag(takes_context=False)
def social_image(page, site):
    image = None

    if isinstance(page, PromoteMixin):
        image = page.get_social_image()

    if image is None:
        image = SocialMediaSettings.for_site(site).default_sharing_image

    if image is not None:
        return image.get_rendition("original").url

    return ""
