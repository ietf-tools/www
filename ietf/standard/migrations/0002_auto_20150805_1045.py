# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.core.fields
import wagtail.core.blocks
import django.db.models.deletion
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0006_add_verbose_names'),
        ('standard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='standardindexpage',
            name='feed_image',
            field=models.ForeignKey(to='wagtailimages.Image', related_name='+', blank=True, null=True, help_text='This image will be used in listings and indexes across the site, if no feed image is added, the social image will be used.', on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='standardindexpage',
            name='in_depth',
            field=wagtail.core.fields.StreamField((('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())), default=[], help_text='Enter the body content for the IN-DEPTH summary tab. This content is for participants and experienced audiences'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='standardindexpage',
            name='introduction',
            field=models.CharField(default=[], max_length=255, help_text='Enter the title to display on the page, you can use only 255 characters.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='standardindexpage',
            name='key_info',
            field=wagtail.core.fields.StreamField((('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())), default=[], help_text='Enter the body content for the KEY INFO summary tab. This content is for non-participating and new audiences'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='standardindexpage',
            name='social_image',
            field=models.ForeignKey(to='wagtailimages.Image', related_name='+', blank=True, null=True, help_text="Image to appear alongside 'social text', particularly for sharing on social networks", on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='standardindexpage',
            name='social_text',
            field=models.CharField(blank=True, max_length=255, help_text='Description of this page as it should appear when shared on social networks, or in Google results'),
        ),
    ]
