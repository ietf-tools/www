# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0016_auto_20151201_1607'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsor',
            name='link',
            field=models.URLField(blank=True),
        ),
    ]
