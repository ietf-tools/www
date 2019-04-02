# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20150817_1726'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpage',
            name='prepared_page_content',
        ),
        migrations.AddField(
            model_name='blogpage',
            name='prepared_body',
            field=models.TextField(blank=True, null=True, help_text='The prepared body content after bibliography styling has been applied. Auto-generated on each save.'),
        ),
    ]
