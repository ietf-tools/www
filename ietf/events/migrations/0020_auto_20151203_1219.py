# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0019_auto_20151203_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpage',
            name='reservations_open',
            field=models.DateField(blank=True, null=True),
        ),
    ]
