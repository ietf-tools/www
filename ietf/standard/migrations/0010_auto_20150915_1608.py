# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('standard', '0009_auto_20150910_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='standardpage',
            name='call_to_action',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, help_text='Specify the page you would like visitors to go to next.', null=True, blank=True, to='snippets.CallToAction'),
        ),
    ]
