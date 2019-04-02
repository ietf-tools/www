# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0012_auto_20151103_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='secondarytopicpage',
            name='area',
            field=models.ForeignKey(related_name='+', null=True, to='datatracker.Area', on_delete=django.db.models.deletion.SET_NULL),
        ),
    ]
