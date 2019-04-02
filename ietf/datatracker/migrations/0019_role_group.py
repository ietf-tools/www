# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datatracker', '0018_rolename_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='group',
            field=models.CharField(default='', max_length=511),
            preserve_default=False,
        ),
    ]
