# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0017_auto_20151202_1645'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eventpage',
            old_name='date',
            new_name='start_date',
        ),
    ]
