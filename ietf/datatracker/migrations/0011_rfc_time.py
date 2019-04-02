# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datatracker', '0010_charter'),
    ]

    operations = [
        migrations.AddField(
            model_name='rfc',
            name='time',
            field=models.CharField(blank=True, max_length=511),
        ),
    ]
