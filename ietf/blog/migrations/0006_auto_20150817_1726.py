# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.images.blocks
import wagtail.core.fields
import wagtail.core.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_blogpage_prepared_page_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpage',
            name='body',
            field=wagtail.core.fields.StreamField((('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())), help_text='The page body text.'),
        ),
        migrations.AlterField(
            model_name='blogpage',
            name='introduction',
            field=models.CharField(max_length=511, help_text='The page introduction text.'),
        ),
    ]
