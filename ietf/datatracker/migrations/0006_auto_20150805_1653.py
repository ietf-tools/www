# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datatracker', '0005_auto_20150805_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rfc',
            name='authors',
            field=models.TextField(blank=True, max_length=511),
        ),
        migrations.AlterField(
            model_name='rfc',
            name='title',
            field=models.TextField(blank=True, max_length=511),
        ),
    ]
