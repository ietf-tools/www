# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0001_initial'),
        ('events', '0023_remove_eventpage_host'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpage',
            name='main_image',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.SET_NULL, to='images.IETFImage', null=True, related_name='+'),
        ),
    ]
