# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ietf.datatracker.models


class Migration(migrations.Migration):

    dependencies = [
        ('datatracker', '0003_auto_20150805_1450'),
    ]

    operations = [
        migrations.CreateModel(
            name='RFC',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('active', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=511)),
                ('resource_uri', models.CharField(max_length=511)),
                ('title', models.CharField(max_length=511)),
                ('rfc', models.CharField(max_length=511)),
                ('authors', models.CharField(max_length=511)),
                ('abstract', models.CharField(max_length=511)),
                ('group', models.CharField(max_length=511)),
            ],
            bases=(ietf.datatracker.models.DatatrackerMixin, models.Model),
        ),
    ]
