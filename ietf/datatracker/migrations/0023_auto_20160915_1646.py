# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datatracker', '0022_auto_20160825_1055'),
    ]

    operations = [
        migrations.AddField(
            model_name='area',
            name='updating',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='charter',
            name='updating',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='email',
            name='updating',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='internetdraft',
            name='updating',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='person',
            name='updating',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='rfc',
            name='updating',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='role',
            name='updating',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='rolename',
            name='updating',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='workinggroup',
            name='updating',
            field=models.BooleanField(default=False),
        ),
    ]
