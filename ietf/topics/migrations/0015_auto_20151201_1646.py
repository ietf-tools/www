# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks
import wagtail.embeds.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0014_auto_20151201_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='primarytopicpage',
            name='in_depth',
            field=wagtail.core.fields.StreamField((('heading', wagtail.core.blocks.CharBlock(icon='title')), ('paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image')), ('embed', wagtail.embeds.blocks.EmbedBlock(icon='code')), ('raw_html', wagtail.core.blocks.RawHTMLBlock(icon='placeholder')))),
        ),
        migrations.AlterField(
            model_name='primarytopicpage',
            name='key_info',
            field=wagtail.core.fields.StreamField((('heading', wagtail.core.blocks.CharBlock(icon='title')), ('paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image')), ('embed', wagtail.embeds.blocks.EmbedBlock(icon='code')), ('raw_html', wagtail.core.blocks.RawHTMLBlock(icon='placeholder')))),
        ),
        migrations.AlterField(
            model_name='secondarytopicpage',
            name='in_depth',
            field=wagtail.core.fields.StreamField((('heading', wagtail.core.blocks.CharBlock(icon='title')), ('paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image')), ('embed', wagtail.embeds.blocks.EmbedBlock(icon='code')), ('raw_html', wagtail.core.blocks.RawHTMLBlock(icon='placeholder')))),
        ),
        migrations.AlterField(
            model_name='secondarytopicpage',
            name='key_info',
            field=wagtail.core.fields.StreamField((('heading', wagtail.core.blocks.CharBlock(icon='title')), ('paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image')), ('embed', wagtail.embeds.blocks.EmbedBlock(icon='code')), ('raw_html', wagtail.core.blocks.RawHTMLBlock(icon='placeholder')))),
        ),
    ]
