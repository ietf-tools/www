# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import wagtail.images.blocks
import django.db.models.deletion
import wagtail.core.fields
import wagtail.core.blocks
import wagtail.documents.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0006_add_verbose_names'),
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventpage',
            name='at_a_glance',
            field=wagtail.core.fields.StreamField((('title', wagtail.core.blocks.CharBlock()), ('link_group', wagtail.core.blocks.StreamBlock((('link', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('link_external', wagtail.core.blocks.URLBlock(required=False)), ('link_page', wagtail.core.blocks.PageChooserBlock(required=False)), ('link_document', wagtail.documents.blocks.DocumentChooserBlock(required=False))))),)))), blank=True),
        ),
        migrations.AddField(
            model_name='eventpage',
            name='body',
            field=wagtail.core.fields.StreamField((('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())), default=[]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eventpage',
            name='date',
            field=models.DateField(default=datetime.date(2015, 1, 1)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eventpage',
            name='feed_image',
            field=models.ForeignKey(related_name='+', to='wagtailimages.Image', help_text='This image will be used in listings and indexes across the site, if no feed image is added, the social image will be used.', blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='eventpage',
            name='introduction',
            field=models.CharField(max_length=511, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eventpage',
            name='main_image',
            field=models.ForeignKey(to='wagtailimages.Image', related_name='+', default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eventpage',
            name='social_image',
            field=models.ForeignKey(related_name='+', to='wagtailimages.Image', help_text="Image to appear alongside 'social text', particularly for sharing on social networks", blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='eventpage',
            name='social_text',
            field=models.CharField(max_length=255, help_text='Description of this page as it should appear when shared on social networks, or in Google results', blank=True),
        ),
    ]
