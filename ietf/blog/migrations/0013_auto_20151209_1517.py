# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_blogpage_author_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpage',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, null=True, to='snippets.Person', related_name='+', blank=True),
        ),
    ]
