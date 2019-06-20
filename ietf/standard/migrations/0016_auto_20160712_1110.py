# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('standard', '0015_auto_20160315_1523'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='standardindexpage',
            options={'verbose_name': 'Index Page'},
        ),
    ]
