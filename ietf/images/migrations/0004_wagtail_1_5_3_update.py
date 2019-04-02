# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.images.models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0003_ietfimage_collection'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ietfrendition',
            name='file',
            field=models.ImageField(width_field='width', upload_to=wagtail.images.models.get_rendition_upload_to, height_field='height'),
        ),
    ]
