# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '006_wagtail_filter_spec'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ietfrendition',
            name='filter_spec',
            field=models.CharField(max_length=255, db_index=True),
        ),
        migrations.AlterField(
            model_name='ietfrendition',
            name='focal_point_key',
            field=models.CharField(editable=False, default='', blank=True, max_length=16),
        ),
        migrations.AlterUniqueTogether(
            name='ietfrendition',
            unique_together=set([('image', 'filter_spec', 'focal_point_key')]),
        ),
    ]
