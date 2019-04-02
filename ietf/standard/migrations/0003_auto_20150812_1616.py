# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('standard', '0002_auto_20150805_1045'),
    ]

    operations = [
        migrations.AddField(
            model_name='standardpage',
            name='area_uri',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='standardpage',
            name='charter_uri',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='standardpage',
            name='internet_draft_uri',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='standardpage',
            name='rfc_uri',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='standardpage',
            name='working_group_uri',
            field=models.URLField(blank=True),
        ),
    ]
