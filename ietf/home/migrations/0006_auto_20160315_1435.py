# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0001_initial'),
        ('home', '0005_auto_20151015_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='main_image',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.SET_NULL, to='images.IETFImage', null=True, related_name='+'),
        ),
    ]
