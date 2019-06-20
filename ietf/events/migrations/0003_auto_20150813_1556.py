# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
import wagtail.core.fields
import wagtail.documents.blocks
import wagtail.core.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20150813_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpage',
            name='at_a_glance',
            field=wagtail.core.fields.StreamField((('item', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('link_group', wagtail.core.blocks.StreamBlock((('link', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('link_external', wagtail.core.blocks.URLBlock(required=False)), ('link_page', wagtail.core.blocks.PageChooserBlock(required=False)), ('link_document', wagtail.documents.blocks.DocumentChooserBlock(required=False))))),)))))),), blank=True),
        ),
    ]
