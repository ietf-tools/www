# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20150811_1128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpage',
            name='date_published',
            field=models.DateTimeField(null=True, help_text='Use this field to override the date that the blog post appears to have been published.', blank=True),
        ),
    ]
