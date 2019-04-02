# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('standard', '0010_auto_20150915_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='standardpage',
            name='prepared_in_depth',
            field=models.TextField(null=True, blank=True, help_text='The prepared in depth field after bibliography styling has been applied. Auto-generated on each save.'),
        ),
        migrations.AddField(
            model_name='standardpage',
            name='prepared_key_info',
            field=models.TextField(null=True, blank=True, help_text='The prepared key info field after bibliography styling has been applied. Auto-generated on each save.'),
        ),
    ]
