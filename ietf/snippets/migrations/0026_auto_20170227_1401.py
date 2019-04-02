# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0025_auto_20160704_1608'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='role',
            options={'verbose_name': 'Role Override', 'ordering': ['name']},
        ),
    ]
