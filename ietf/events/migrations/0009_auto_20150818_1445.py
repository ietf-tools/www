# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.core.fields
import wagtail.images.blocks
import wagtail.core.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_auto_20150814_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpage',
            name='body',
            field=wagtail.core.fields.StreamField((('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())), help_text='The main text describing the event.'),
        ),
        migrations.AlterField(
            model_name='eventpage',
            name='date',
            field=models.DateField(help_text='The date of the event.'),
        ),
        migrations.AlterField(
            model_name='eventpage',
            name='introduction',
            field=models.CharField(max_length=511, help_text='The introduction for the event page. Limited to 511 characters.'),
        ),
    ]
