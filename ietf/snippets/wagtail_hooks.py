from django.conf.urls import include, url
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.urlresolvers import reverse
from django.utils.html import format_html, format_html_join
from wagtail.core import hooks
from wagtail.admin.rich_text import HalloPlugin

from ietf.datatracker.link_choosers import RFCLinkChooser
from . import admin_urls


@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        url(r'^snippet-link/', include(admin_urls, app_name='snippetlink', namespace='snippet_link')),
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
        reverse('snippet_link:chooser', kwargs={'snippet_type': RFCLinkChooser.link_type})
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
