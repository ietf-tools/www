# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_auto_20160127_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpage',
            name='feed_image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, help_text='This image will be used in listings and indexes across the site, if no feed image is added, the social image will be used.', blank=True, related_name='+', to='images.IETFImage'),
        ),
        migrations.AlterField(
            model_name='blogpage',
            name='social_image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, help_text="Image to appear alongside 'social text', particularly for sharing on social networks", blank=True, related_name='+', to='images.IETFImage'),
        ),
    ]
