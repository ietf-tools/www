# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datatracker', '0021_datatrackermeta'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='area',
            options={'verbose_name': 'Area', 'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='email',
            options={'verbose_name': 'Email'},
        ),
        migrations.AlterModelOptions(
            name='person',
            options={'verbose_name': 'Person', 'ordering': ['name'], 'verbose_name_plural': 'People'},
        ),
        migrations.AlterModelOptions(
            name='role',
            options={'verbose_name': 'Role'},
        ),
        migrations.AlterModelOptions(
            name='rolename',
            options={'verbose_name': 'Role Name'},
        ),
        migrations.AlterModelOptions(
            name='workinggroup',
            options={'verbose_name': 'Working Group', 'ordering': ['name']},
        ),
    ]
