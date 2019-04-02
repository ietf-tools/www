# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datatracker', '0019_role_group'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='person',
            options={'verbose_name_plural': 'People', 'ordering': ['name']},
        ),
    ]
