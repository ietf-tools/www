from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.core import urls as wagtail_urls

from ietf.datatracker import urls as datatracker_urls
from ietf.bibliography import urls as bibliography_urls
from ietf.search.views import search
from ietf.snippets import urls as snippet_urls
from ietf.blog.feeds import BlogFeed

urlpatterns = [
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^bibliography/', include(bibliography_urls)),
    url(r'^django-admin/', include(admin.site.urls)),
    url(r'^blog/feed/$', BlogFeed(), name='blog_feed'),

    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),

    url(r'^search/$', search, name='search'),
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
        url(r'^test404/$', TemplateView.as_view(template_name='404.html')),
        url(r'^test500/$', TemplateView.as_view(template_name='500.html')),
    ]


urlpatterns += [
    url(r'^datatracker/', include(datatracker_urls)),
    url(r'^misc/', include(snippet_urls)),
    url(r'', include(wagtail_urls)),
]
