from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django.shortcuts import render
from wagtail.models import Page

from .models import BibliographyItem


def referenced_types(request):
    content_types = (
        BibliographyItem.objects.exclude(content_type=None)
        .order_by()
        .values_list("content_type")
        .distinct()
        .annotate(num=Count("content_type"))
        .order_by("-num")
    )
    return render(
        request,
        "bibliography/referenced_types.html",
        {
            "types": [
                (ContentType.objects.get(pk=type_id), count)
                for type_id, count in content_types
            ]
        },
    )


def referenced_objects(request, content_type_id):
    content_type = ContentType.objects.get(pk=content_type_id)
    object_ids = (
        BibliographyItem.objects.filter(content_type=content_type_id)
        .order_by()
        .values_list("object_id")
        .distinct()
        .annotate(num=Count("object_id"))
        .order_by("-num")
    )
    return render(
        request,
        "bibliography/referenced_objects.html",
        {
            "title": content_type._meta.verbose_name,
            "content_type_id": content_type_id,
            "objects": [
                (content_type.get_object_for_this_type(id=object_id), count)
                for object_id, count in object_ids
            ],
        },
    )


def referencing_pages(request, content_type_id, object_id):
    content_type = ContentType.objects.get(pk=content_type_id)
    obj = content_type.get_object_for_this_type(id=object_id)
    page_ids = BibliographyItem.objects.filter(
        content_type=content_type_id, object_id=object_id
    ).values_list("page", flat=True)
    pages = Page.objects.filter(pk__in=page_ids)
    return render(
        request,
        "bibliography/referencing_pages.html",
        {"title": obj.__str__(), "pages": pages},
    )
