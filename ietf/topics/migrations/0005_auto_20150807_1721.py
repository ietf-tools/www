# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0006_add_verbose_names'),
        ('topics', '0004_auto_20150807_1600'),
    ]

    operations = [
        migrations.AddField(
            model_name='topicindexpage',
            name='feed_image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, related_name='+', help_text='This image will be used in listings and indexes across the site, if no feed image is added, the social image will be used.', blank=True, to='wagtailimages.Image', null=True),
        ),
        migrations.AddField(
            model_name='topicindexpage',
            name='introduction',
            field=models.CharField(max_length=255, help_text='Enter the title to display on the page, you can use only 255 characters.', default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='topicindexpage',
            name='social_image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, related_name='+', help_text="Image to appear alongside 'social text', particularly for sharing on social networks", blank=True, to='wagtailimages.Image', null=True),
        ),
        migrations.AddField(
            model_name='topicindexpage',
            name='social_text',
            field=models.CharField(max_length=255, help_text='Description of this page as it should appear when shared on social networks, or in Google results', blank=True),
        ),
    ]
