# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0005_auto_20161115_1458'),
    ]

    operations = [
        migrations.AddField(
            model_name='footerlinkitem',
            name='title',
            field=models.CharField(max_length=255, default=''),
            preserve_default=False,
        ),
    ]
