# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.images.blocks
import wagtail.embeds.blocks
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20150929_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpage',
            name='body',
            field=wagtail.core.fields.StreamField((('heading', wagtail.core.blocks.CharBlock(classname='full title', icon='title')), ('paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image')), ('embed', wagtail.embeds.blocks.EmbedBlock(icon='arrow-right'))), help_text='The page body text.'),
        ),
    ]
