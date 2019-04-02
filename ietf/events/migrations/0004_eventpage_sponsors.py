# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.core.fields
import ietf.snippets.models
import wagtail.core.blocks
import wagtail.snippets.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20150813_1556'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventpage',
            name='sponsors',
            field=wagtail.core.fields.StreamField((('sponsor_category', wagtail.core.blocks.StructBlock((('category_title', wagtail.core.blocks.CharBlock()), ('sponsor_group', wagtail.core.blocks.StreamBlock((('sponsor', wagtail.snippets.blocks.SnippetChooserBlock(ietf.snippets.models.Sponsor)),)))))),), blank=True),
        ),
    ]
