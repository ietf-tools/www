# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ietf.datatracker.models


class Migration(migrations.Migration):

    dependencies = [
        ('datatracker', '0002_area_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkingGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('active', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=511)),
                ('resource_uri', models.CharField(max_length=511)),
                ('parent', models.CharField(blank=True, max_length=511)),
                ('description', models.CharField(blank=True, max_length=511)),
                ('comments', models.CharField(blank=True, max_length=511)),
                ('charter', models.CharField(blank=True, max_length=511)),
            ],
            bases=(ietf.datatracker.models.DatatrackerMixin, models.Model),
        ),
        migrations.AddField(
            model_name='area',
            name='resource_uri',
            field=models.CharField(default='', max_length=511),
            preserve_default=False,
        ),
    ]
