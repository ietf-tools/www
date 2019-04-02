# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0023_group_role'),
        ('events', '0021_eventpage_venue_section_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventPageHost',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('host', models.ForeignKey(null=True, to='snippets.Sponsor', related_name='+', blank=True, on_delete=django.db.models.deletion.SET_NULL)),
                ('page', modelcluster.fields.ParentalKey(to='events.EventPage', related_name='hosts')),
            ],
        ),
    ]
