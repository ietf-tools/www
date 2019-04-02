# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datatracker', '0023_auto_20160915_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workinggroup',
            name='comments',
            field=models.CharField(blank=True, max_length=4096),
        ),
        migrations.AlterField(
            model_name='workinggroup',
            name='description',
            field=models.CharField(blank=True, max_length=4096),
        ),
    ]
