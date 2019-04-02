# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0006_add_verbose_names'),
        ('events', '0006_auto_20150813_1801'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventlistingpage',
            name='feed_image',
            field=models.ForeignKey(to='wagtailimages.Image', help_text='This image will be used in listings and indexes across the site, if no feed image is added, the social image will be used.', related_name='+', blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='eventlistingpage',
            name='social_image',
            field=models.ForeignKey(to='wagtailimages.Image', help_text="Image to appear alongside 'social text', particularly for sharing on social networks", related_name='+', blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='eventlistingpage',
            name='social_text',
            field=models.CharField(max_length=255, help_text='Description of this page as it should appear when shared on social networks, or in Google results', blank=True),
        ),
    ]
