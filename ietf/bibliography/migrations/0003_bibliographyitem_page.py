# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0001_squashed_0016_change_page_url_path_to_text_field'),
        ('bibliography', '0002_bibliographyitem_content_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='bibliographyitem',
            name='page',
            field=models.ForeignKey(help_text='The page that this item links to.', related_name='bibliography_items', default=1, to='wagtailcore.Page'),
            preserve_default=False,
        ),
    ]
