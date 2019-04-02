# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0006_sponsor'),
        ('events', '0007_auto_20150813_1803'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventpage',
            name='host',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, related_name='+', null=True, blank=True, to='snippets.Sponsor'),
        ),
        migrations.AddField(
            model_name='eventpage',
            name='listing_location',
            field=models.CharField(help_text='Add a short location name to appear on the event listing.', max_length=255, blank=True),
        ),
    ]
