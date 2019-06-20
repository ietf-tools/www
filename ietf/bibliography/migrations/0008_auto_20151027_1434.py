# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('bibliography', '0007_remove_bibliographytestpage_prepared_page_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bibliographyitem',
            name='page',
            field=modelcluster.fields.ParentalKey(to='wagtailcore.Page', help_text='The page that this item links to.', related_name='bibliography_items'),
        ),
    ]
