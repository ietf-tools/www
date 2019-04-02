# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datatracker', '0008_internetdraft'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internetdraft',
            name='abstract',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='internetdraft',
            name='authors',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='internetdraft',
            name='title',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='rfc',
            name='abstract',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='rfc',
            name='authors',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='rfc',
            name='title',
            field=models.TextField(blank=True),
        ),
    ]
