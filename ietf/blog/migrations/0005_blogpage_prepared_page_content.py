# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20150811_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpage',
            name='prepared_page_content',
            field=models.TextField(blank=True, null=True, help_text='The prepared page content after bibliography styling has been applied. Auto-generated on each save.'),
        ),
    ]
