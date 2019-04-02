# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bibliography', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bibliographyitem',
            name='content_key',
            field=models.CharField(default='', max_length=127, help_text='The "key" with which this item was created, eg. "rfc" in [[rfc:3514]].'),
            preserve_default=False,
        ),
    ]
