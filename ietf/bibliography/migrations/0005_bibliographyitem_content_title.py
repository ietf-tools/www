# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bibliography', '0004_bibliographytestpage'),
    ]

    operations = [
        migrations.AddField(
            model_name='bibliographyitem',
            name='content_title',
            field=models.CharField(help_text='The link title for this item, eg. "RFC 7168" for [[rfc:7168]].', default='', max_length=127),
            preserve_default=False,
        ),
    ]
