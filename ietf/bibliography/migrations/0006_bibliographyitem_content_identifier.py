# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bibliography', '0005_bibliographyitem_content_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='bibliographyitem',
            name='content_identifier',
            field=models.CharField(help_text='The "value" with which this item was created, eg. "3514" in [[rfc:3514]].', default=1, max_length=127),
            preserve_default=False,
        ),
    ]
