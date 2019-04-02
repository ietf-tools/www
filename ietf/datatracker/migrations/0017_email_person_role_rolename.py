# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ietf.datatracker.models
import wagtail.search.index


class Migration(migrations.Migration):

    dependencies = [
        ('datatracker', '0016_auto_20151028_1532'),
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=False)),
                ('resource_uri', models.CharField(max_length=511)),
                ('address', models.CharField(max_length=511)),
                ('person', models.CharField(max_length=511)),
            ],
            bases=(ietf.datatracker.models.DatatrackerMixin, models.Model, wagtail.search.index.Indexed),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=511)),
                ('biography', models.TextField(blank=True)),
                ('resource_uri', models.CharField(max_length=511)),
                ('photo', models.CharField(max_length=511)),
                ('photo_thumb', models.CharField(max_length=511)),
            ],
            options={
                'verbose_name': 'People',
                'ordering': ['name'],
            },
            bases=(ietf.datatracker.models.DatatrackerMixin, models.Model, wagtail.search.index.Indexed),
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=False)),
                ('email', models.CharField(max_length=511)),
                ('name', models.CharField(max_length=511)),
                ('person', models.CharField(max_length=511)),
                ('resource_uri', models.CharField(max_length=511)),
            ],
            bases=(ietf.datatracker.models.DatatrackerMixin, models.Model, wagtail.search.index.Indexed),
        ),
        migrations.CreateModel(
            name='RoleName',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=511)),
                ('resource_uri', models.CharField(max_length=511)),
            ],
            bases=(ietf.datatracker.models.DatatrackerMixin, models.Model, wagtail.search.index.Indexed),
        ),
    ]
