# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0020_auto_20151203_1219'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventpage',
            name='venue_section_title',
            field=models.CharField(default='Meeting venue information', max_length=255),
        ),
    ]
