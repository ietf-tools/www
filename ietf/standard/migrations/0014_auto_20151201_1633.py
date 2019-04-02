# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.images.blocks
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('standard', '0013_auto_20151103_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='standardindexpage',
            name='in_depth',
            field=wagtail.core.fields.StreamField((('heading', wagtail.core.blocks.CharBlock(icon='title')), ('paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image')), ('embed', wagtail.embeds.blocks.EmbedBlock(icon='code')), ('raw_html', wagtail.core.blocks.RawHTMLBlock(icon='placeholder')))),
        ),
        migrations.AlterField(
            model_name='standardindexpage',
            name='key_info',
            field=wagtail.core.fields.StreamField((('heading', wagtail.core.blocks.CharBlock(icon='title')), ('paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image')), ('embed', wagtail.embeds.blocks.EmbedBlock(icon='code')), ('raw_html', wagtail.core.blocks.RawHTMLBlock(icon='placeholder')))),
        ),
        migrations.AlterField(
            model_name='standardpage',
            name='in_depth',
            field=wagtail.core.fields.StreamField((('heading', wagtail.core.blocks.CharBlock(icon='title')), ('paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image')), ('embed', wagtail.embeds.blocks.EmbedBlock(icon='code')), ('raw_html', wagtail.core.blocks.RawHTMLBlock(icon='placeholder')))),
        ),
        migrations.AlterField(
            model_name='standardpage',
            name='key_info',
            field=wagtail.core.fields.StreamField((('heading', wagtail.core.blocks.CharBlock(icon='title')), ('paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image')), ('embed', wagtail.embeds.blocks.EmbedBlock(icon='code')), ('raw_html', wagtail.core.blocks.RawHTMLBlock(icon='placeholder')))),
        ),
    ]
