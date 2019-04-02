# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0019_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='title',
        ),
    ]
