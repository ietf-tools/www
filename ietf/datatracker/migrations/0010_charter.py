# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ietf.datatracker.models


class Migration(migrations.Migration):

    dependencies = [
        ('datatracker', '0009_auto_20150806_1523'),
    ]

    operations = [
        migrations.CreateModel(
            name='Charter',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('active', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=511)),
                ('resource_uri', models.CharField(max_length=511)),
                ('title', models.TextField(blank=True)),
                ('authors', models.TextField(blank=True)),
                ('abstract', models.TextField(blank=True)),
                ('group', models.CharField(max_length=511)),
            ],
            bases=(ietf.datatracker.models.DatatrackerMixin, models.Model),
        ),
    ]
