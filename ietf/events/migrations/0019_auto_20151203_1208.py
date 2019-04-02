# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0018_auto_20151203_1205'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventpage',
            name='end_date',
            field=models.DateField(null=True, blank=True, help_text='The end date of the event.'),
        ),
        migrations.AlterField(
            model_name='eventpage',
            name='start_date',
            field=models.DateField(null=True, blank=True, help_text='The start date date of the event.'),
        ),
    ]
