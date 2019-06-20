# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0009_auto_20150814_1655'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='calltoaction',
            options={'verbose_name_plural': 'Calls to action'},
        ),
    ]
