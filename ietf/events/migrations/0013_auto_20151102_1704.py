# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.images.blocks
import wagtail.embeds.blocks
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0012_auto_20150915_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpage',
            name='body',
            field=wagtail.core.fields.StreamField((('heading', wagtail.core.blocks.CharBlock(classname='full title', icon='title')), ('paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image')), ('embed', wagtail.embeds.blocks.EmbedBlock(icon='arrow-right'))), help_text='The main text describing the event.'),
        ),
    ]
