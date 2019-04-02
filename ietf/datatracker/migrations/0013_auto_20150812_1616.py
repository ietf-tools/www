# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datatracker', '0012_auto_20150807_1224'),
    ]

    operations = [
        migrations.AddField(
            model_name='area',
            name='acronym',
            field=models.CharField(blank=True, max_length=511),
        ),
        migrations.AddField(
            model_name='area',
            name='list_email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='area',
            name='list_subscribe',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]
