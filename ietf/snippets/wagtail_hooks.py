from django.conf.urls import include, url
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.urls import reverse
from django.utils.html import format_html, format_html_join

from wagtail.admin.menu import MenuItem
from wagtail.admin.rich_text import HalloPlugin
from wagtail.admin.rich_text.converters import editor_html
from wagtail.core import hooks

from . import admin_urls
from .link_choosers import (
    ExternalRichTextLinkHandler,
    GlossaryItemLinkChooser,
    GlossaryItemRichTextLinkHandler,
    RFCLinkChooser,
    RFCRichTextLinkHandler,
    CharterLinkChooser,
    CharterRichTextLinkHandler,
)


@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        url(r'^snippet-link/', include(admin_urls, namespace='snippet_link')),
    ]

@hooks.register('insert_editor_js')
def editor_js():
    js_files = [
        static('snippet_linker/js/snippet-chooser.js'),
    ]
    js_includes = format_html_join(
        '\n', '<script src="{0}"></script>',
        ((filename, ) for filename in js_files)
    )

    return js_includes + format_html(
        """
        <script>
            window.chooserUrls.snippetLinkChooser = '{0}';
        </script>
        """,
        reverse('snippet_link:chooser', kwargs={'snippet_type': GlossaryItemLinkChooser.link_type})
    )

@hooks.register('register_rich_text_features')
def register_embed_feature(features):
    features.register_editor_plugin(
        'hallo', 'snippet',
        HalloPlugin(
            name='hallowagtailsnippetlink',
            js=['snippet_linker/js/hallo-plugins/hallo-wagtailsnippetlink.js'],
        )
    )
    features.default_features.append('snippet')
    features.default_features.append('h5')


@hooks.register('register_link_chooser')
def register_glosary_item_link_chooser():
    return GlossaryItemLinkChooser()

@hooks.register('register_link_chooser')
def register_rfc_link_chooser():
    return RFCLinkChooser()

@hooks.register('register_link_chooser')
def register_charter_link_chooser():
    return CharterLinkChooser()


@hooks.register('register_rich_text_features')
def register_link_choosers(features):
    # Register conversion rules for translating between database and hallo.js
    features.register_converter_rule(
        'editorhtml', 'snippet', [
            editor_html.LinkTypeRule(RFCRichTextLinkHandler.link_type, RFCRichTextLinkHandler),
            editor_html.LinkTypeRule(CharterRichTextLinkHandler.link_type, CharterRichTextLinkHandler),
            editor_html.LinkTypeRule(GlossaryItemRichTextLinkHandler.link_type, GlossaryItemRichTextLinkHandler),
            editor_html.LinkTypeRule(ExternalRichTextLinkHandler.link_type, ExternalRichTextLinkHandler),
            editor_html.LinkTypeRule('email', ExternalRichTextLinkHandler),
        ]
    )

    # Register conversion rules for translating from database to frontend.
    # Here we re-use the conversion function from hallo.js (which means that the data-foo
    # attributes also get added, which may or may not be a good thing.)
    features.register_link_type(GlossaryItemRichTextLinkHandler.link_type, GlossaryItemRichTextLinkHandler.expand_db_attributes)
    features.register_link_type(RFCRichTextLinkHandler.link_type, RFCRichTextLinkHandler.expand_db_attributes)
    features.register_link_type(CharterRichTextLinkHandler.link_type, CharterRichTextLinkHandler.expand_db_attributes)
