# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.core.blocks
import wagtail.images.blocks
import wagtail.core.fields
import wagtail.embeds.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0020_auto_20160712_1110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='primarytopicpage',
            name='in_depth',
            field=wagtail.core.fields.StreamField((('heading', wagtail.core.blocks.CharBlock(icon='title')), ('paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('image', wagtail.images.blocks.ImageChooserBlock(template='includes/imageblock.html', icon='image')), ('embed', wagtail.embeds.blocks.EmbedBlock(icon='code')), ('raw_html', wagtail.core.blocks.RawHTMLBlock(icon='placeholder')))),
        ),
        migrations.AlterField(
            model_name='primarytopicpage',
            name='key_info',
            field=wagtail.core.fields.StreamField((('heading', wagtail.core.blocks.CharBlock(icon='title')), ('paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('image', wagtail.images.blocks.ImageChooserBlock(template='includes/imageblock.html', icon='image')), ('embed', wagtail.embeds.blocks.EmbedBlock(icon='code')), ('raw_html', wagtail.core.blocks.RawHTMLBlock(icon='placeholder')))),
        ),
        migrations.AlterField(
            model_name='secondarytopicpage',
            name='in_depth',
            field=wagtail.core.fields.StreamField((('heading', wagtail.core.blocks.CharBlock(icon='title')), ('paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('image', wagtail.images.blocks.ImageChooserBlock(template='includes/imageblock.html', icon='image')), ('embed', wagtail.embeds.blocks.EmbedBlock(icon='code')), ('raw_html', wagtail.core.blocks.RawHTMLBlock(icon='placeholder')))),
        ),
        migrations.AlterField(
            model_name='secondarytopicpage',
            name='key_info',
            field=wagtail.core.fields.StreamField((('heading', wagtail.core.blocks.CharBlock(icon='title')), ('paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('image', wagtail.images.blocks.ImageChooserBlock(template='includes/imageblock.html', icon='image')), ('embed', wagtail.embeds.blocks.EmbedBlock(icon='code')), ('raw_html', wagtail.core.blocks.RawHTMLBlock(icon='placeholder')))),
        ),
    ]
