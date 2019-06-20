# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0016_auto_20151201_1646'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eventpage',
            old_name='at_a_glance',
            new_name='key_details',
        ),
    ]
