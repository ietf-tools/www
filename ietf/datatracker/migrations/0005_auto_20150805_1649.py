# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datatracker', '0004_rfc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rfc',
            name='abstract',
            field=models.TextField(max_length=511, blank=True),
        ),
    ]
