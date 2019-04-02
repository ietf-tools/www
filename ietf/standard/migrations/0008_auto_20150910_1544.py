# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.core.blocks
import wagtail.images.blocks
import wagtail.embeds.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('standard', '0007_auto_20150820_2226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='standardindexpage',
            name='in_depth',
            field=wagtail.core.fields.StreamField((('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('embed', wagtail.embeds.blocks.EmbedBlock())), help_text='Enter the body content for the IN-DEPTH summary tab. This content is for participants and experienced audiences'),
        ),
        migrations.AlterField(
            model_name='standardindexpage',
            name='key_info',
            field=wagtail.core.fields.StreamField((('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('embed', wagtail.embeds.blocks.EmbedBlock())), help_text='Enter the body content for the KEY INFO summary tab. This content is for non-participating and new audiences'),
        ),
        migrations.AlterField(
            model_name='standardpage',
            name='in_depth',
            field=wagtail.core.fields.StreamField((('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('embed', wagtail.embeds.blocks.EmbedBlock())), help_text='Enter the body content for the IN-DEPTH summary tab. This content is for participants and experienced audiences'),
        ),
        migrations.AlterField(
            model_name='standardpage',
            name='key_info',
            field=wagtail.core.fields.StreamField((('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('embed', wagtail.embeds.blocks.EmbedBlock())), help_text='Enter the body content for the KEY INFO summary tab. This content is for non-participating and new audiences'),
        ),
    ]
