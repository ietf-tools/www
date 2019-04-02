# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20150813_1712'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventListingPagePromotedEvent',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
            ],
        ),
        migrations.AddField(
            model_name='eventlistingpage',
            name='introduction',
            field=models.CharField(max_length=511, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eventlistingpagepromotedevent',
            name='page',
            field=modelcluster.fields.ParentalKey(related_name='promoted_events', to='events.EventListingPage'),
        ),
        migrations.AddField(
            model_name='eventlistingpagepromotedevent',
            name='promoted_event',
            field=models.ForeignKey(related_name='+', to='events.EventPage'),
        ),
    ]
