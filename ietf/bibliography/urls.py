from django.conf.urls import url

from .views import (
    referenced_types,
    referenced_objects,
    referencing_pages,
)


urlpatterns = [
    url(r'^referenced_types/$', referenced_types, name='referenced_types'),
    url(r'^referenced_objects/(\d+)/$', referenced_objects, name='referenced_objects'),
    url(r'^referencing_pages/(\d+)/(\d+)/$', referencing_pages, name='referencing_pages'),
 ]
