# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0008_image_created_at_index'),
        ('home', '0003_auto_20150915_1103'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='main_image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='wagtailimages.Image', related_name='+', blank=True),
        ),
    ]
