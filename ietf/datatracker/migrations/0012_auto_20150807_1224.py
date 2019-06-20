# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datatracker', '0011_rfc_time'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='area',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='charter',
            options={'ordering': ['title']},
        ),
        migrations.AlterModelOptions(
            name='internetdraft',
            options={'ordering': ['title']},
        ),
        migrations.AlterModelOptions(
            name='rfc',
            options={'ordering': ['title']},
        ),
        migrations.AlterModelOptions(
            name='workinggroup',
            options={'ordering': ['name']},
        ),
    ]
