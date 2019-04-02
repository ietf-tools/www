from django import template


register = template.Library()


@register.inclusion_tag("bibliography/bibliography.html")
def bibliography(page):
    """
    Render the bibliography of a page.

    Uses the template "bibliography/bibliography.html" as its framework. The items are put into a variable "items", no
    other variables are available.
    """

    items = []
    for item in page.bibliography_items.all().order_by('ordering'):
        items.append({
            'title': item.render_title(),
            'long_title': item.content_long_title,
            'content': item.render(),
            'ordering': item.ordering,
            'uri': item.render_uri
        })

    return {'items': items}
