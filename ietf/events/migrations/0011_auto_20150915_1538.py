# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_eventpage_reservations_open'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpage',
            name='introduction',
            field=models.CharField(help_text='The introduction for the event page. Limited to 511 characters.', max_length=200),
        ),
    ]
