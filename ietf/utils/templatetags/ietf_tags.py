from urllib.parse import quote

from django.template import Library

from wagtail.core.models import Site

from ..models import SocialMediaSettings


register = Library()


@register.simple_tag(takes_context=False)
def social_text(page, site, encode=False):
    text = ""

    if page and site:
        try:
            text = page.social_text
        except (AttributeError, ValueError):
            text = SocialMediaSettings.for_site(site).default_sharing_text

        if encode:
            text = quote(text)

    return text



@register.simple_tag(takes_context=False)
def social_image(page, site):
    image = ""

    if page and site:
        try:
            image = page.social_image.get_rendition('original').url
        except (AttributeError, ValueError):
            try:
                image = SocialMediaSettings.for_site(
                    site
                ).default_sharing_image.get_rendition('original').url
            except (AttributeError, ValueError):
                pass

    if image:
        image = Site.objects.get(is_default_site=True).root_url + image

    return image
