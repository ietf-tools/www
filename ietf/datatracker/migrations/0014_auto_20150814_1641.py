# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datatracker', '0013_auto_20150812_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='workinggroup',
            name='list_email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='workinggroup',
            name='list_subscribe',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]
