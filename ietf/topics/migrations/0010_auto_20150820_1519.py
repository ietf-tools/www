# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0009_auto_20150818_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='primarytopicpage',
            name='call_to_action',
            field=models.ForeignKey(to='snippets.CallToAction', related_name='+', on_delete=django.db.models.deletion.SET_NULL, help_text='Will only be displayed if no mailing list signup is selected.', null=True, blank=True),
        ),
    ]
