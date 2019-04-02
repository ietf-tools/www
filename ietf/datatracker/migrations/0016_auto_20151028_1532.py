# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datatracker', '0015_auto_20151028_1524'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='charter',
            options={'ordering': ['title'], 'verbose_name': 'Charter'},
        ),
        migrations.AlterModelOptions(
            name='internetdraft',
            options={'ordering': ['title'], 'verbose_name': 'Internet Draft'},
        ),
    ]
