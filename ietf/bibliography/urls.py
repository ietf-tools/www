from django.urls import re_path

from .views import (
    referenced_types,
    referenced_objects,
    referencing_pages,
)


urlpatterns = [
    re_path(r"^referenced_types/$", referenced_types, name="referenced_types"),
    re_path(
        r"^referenced_objects/(\d+)/$", referenced_objects, name="referenced_objects"
    ),
    re_path(
        r"^referencing_pages/(\d+)/(\d+)/$", referencing_pages, name="referencing_pages"
    ),
]
