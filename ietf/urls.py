from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
from django.urls import path, re_path
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.documents import urls as wagtaildocs_urls

from ietf.bibliography import urls as bibliography_urls
from ietf.blog.feeds import BlogFeed, TopicBlogFeed
from ietf.search.views import search
from ietf.snippets import urls as snippet_urls

handler500 = "ietf.views.server_error"


urlpatterns = [
    path("sitemap.xml", sitemap),
    re_path(r"^admin/doc/", include("django.contrib.admindocs.urls")),
    re_path(r"^bibliography/", include(bibliography_urls)),
    re_path(r"^django-admin/", admin.site.urls),
    re_path(r"^blog/feed/$", BlogFeed(), name="blog_feed"),
    re_path(r"^blog/(?P<topic>.+)/feed/$", TopicBlogFeed(), name="blog_feed_with_topic"),
    re_path(r"^admin/", include(wagtailadmin_urls)),
    re_path(r"^documents/", include(wagtaildocs_urls)),
    re_path(r"^search/$", search, name="search"),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.views.generic import TemplateView

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Add views for testing 404 and 500 templates
    urlpatterns += [
        re_path(r"^test404/$", TemplateView.as_view(template_name="404.html")),
        re_path(r"^test500/$", TemplateView.as_view(template_name="500.html")),
    ]


urlpatterns += [
    re_path(r"^misc/", include(snippet_urls)),
    re_path(r"", include(wagtail_urls)),
]
