# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0019_group'),
        ('blog', '0011_auto_20151201_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpage',
            name='author_group',
            field=models.ForeignKey(null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='snippets.Group'),
        ),
    ]
