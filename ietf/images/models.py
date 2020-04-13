from django.db import models

from wagtail.images.models import Image, AbstractImage, AbstractRendition


class IETFImage(AbstractImage):
    caption = models.CharField(max_length=255, null=True, blank=True)

    admin_form_fields = Image.admin_form_fields + (
        'caption',
    )


class IETFRendition(AbstractRendition):
    image = models.ForeignKey(IETFImage, related_name='renditions', on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )
