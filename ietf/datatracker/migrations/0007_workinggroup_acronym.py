# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datatracker', '0006_auto_20150805_1653'),
    ]

    operations = [
        migrations.AddField(
            model_name='workinggroup',
            name='acronym',
            field=models.CharField(blank=True, max_length=511),
        ),
    ]
