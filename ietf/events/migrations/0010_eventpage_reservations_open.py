# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_auto_20150818_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventpage',
            name='reservations_open',
            field=models.DateField(null=True),
        ),
    ]
