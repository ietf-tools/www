# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ietf.datatracker.models


class Migration(migrations.Migration):

    dependencies = [
        ('datatracker', '0007_workinggroup_acronym'),
    ]

    operations = [
        migrations.CreateModel(
            name='InternetDraft',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('active', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=511)),
                ('resource_uri', models.CharField(max_length=511)),
                ('title', models.TextField(max_length=511, blank=True)),
                ('authors', models.TextField(max_length=511, blank=True)),
                ('abstract', models.TextField(max_length=511, blank=True)),
                ('group', models.CharField(max_length=511)),
            ],
            bases=(ietf.datatracker.models.DatatrackerMixin, models.Model),
        ),
    ]
