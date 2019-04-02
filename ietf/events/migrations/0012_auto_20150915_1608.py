# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_auto_20150915_1538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpage',
            name='main_image',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, null=True, blank=True, to='wagtailimages.Image'),
        ),
    ]
