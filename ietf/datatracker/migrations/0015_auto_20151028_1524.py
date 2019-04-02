# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datatracker', '0014_auto_20150814_1641'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rfc',
            options={'ordering': ['title'], 'verbose_name': 'RFC'},
        ),
    ]
