# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bibliography', '0008_auto_20151027_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bibliographyitem',
            name='page',
            field=models.ForeignKey(related_name='bibliography_items', to='wagtailcore.Page', help_text='The page that this item links to.'),
        ),
    ]
