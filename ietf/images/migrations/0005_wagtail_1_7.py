# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0004_wagtail_1_5_3_update'),
    ]

    operations = [
        migrations.AddField(
            model_name='ietfrendition',
            name='filter_spec',
            field=models.CharField(max_length=255, default='', blank=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='ietfrendition',
            name='filter',
            field=models.ForeignKey(related_name='+', to='wagtailimages.Filter', null=True, blank=True),
        ),
    ]
