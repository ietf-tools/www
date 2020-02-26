from django.core.urlresolvers import reverse
from wagtail.admin.menu import MenuItem
from wagtail.core import hooks
from wagtail.admin.rich_text.converters import editor_html

from .link_choosers import (
    ExternalRichTextLinkHandler,
    GlossaryItemLinkChooser,
    GlossaryItemRichTextLinkHandler,
)

@hooks.register('register_link_chooser')
def register_glosary_item_link_chooser():
    return GlossaryItemLinkChooser()


@hooks.register('register_rich_text_features')
def register_link_choosers(features):
    # Register conversion rules for translating between database and hallo.js
    features.register_converter_rule(
        'editorhtml', 'snippet', [
            editor_html.LinkTypeRule(GlossaryItemRichTextLinkHandler.link_type, GlossaryItemRichTextLinkHandler),
            editor_html.LinkTypeRule(ExternalRichTextLinkHandler.link_type, ExternalRichTextLinkHandler),
            editor_html.LinkTypeRule('email', ExternalRichTextLinkHandler),
        ]
    )

    # Register conversion rules for translating from database to frontend.
    # Here we re-use the conversion function from hallo.js (which means that the data-foo
    # attributes also get added, which may or may not be a good thing.)
    features.register_link_type(GlossaryItemRichTextLinkHandler.link_type, GlossaryItemRichTextLinkHandler.expand_db_attributes)

