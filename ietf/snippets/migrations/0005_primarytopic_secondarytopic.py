# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0006_auto_20150810_1148'),
        ('snippets', '0004_auto_20150807_1230'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrimaryTopic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=255)),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, null=True, related_name='+', editable=False, to='topics.PrimaryTopicPage')),
            ],
        ),
        migrations.CreateModel(
            name='SecondaryTopic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=255)),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, null=True, related_name='+', editable=False, to='topics.SecondaryTopicPage')),
            ],
        ),
    ]
