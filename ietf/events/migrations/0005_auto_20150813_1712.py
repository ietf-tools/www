# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.core.fields
import wagtail.core.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_eventpage_sponsors'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventpage',
            name='contact_details',
            field=wagtail.core.fields.StreamField((('contact_detail', wagtail.core.blocks.CharBlock(classname='full title')),), blank=True),
        ),
        migrations.AddField(
            model_name='eventpage',
            name='extras',
            field=wagtail.core.fields.StreamField((('extra', wagtail.core.blocks.CharBlock(classname='full title')),), blank=True),
        ),
        migrations.AddField(
            model_name='eventpage',
            name='reservation_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='eventpage',
            name='room_rates',
            field=wagtail.core.fields.StreamField((('room_rate', wagtail.core.blocks.CharBlock(classname='full title')),), blank=True),
        ),
        migrations.AddField(
            model_name='eventpage',
            name='venue',
            field=wagtail.core.fields.StreamField((('address_line', wagtail.core.blocks.CharBlock(classname='full title')),), blank=True),
        ),
    ]
