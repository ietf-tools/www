# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0015_auto_20151201_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='glossaryitem',
            name='link',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='bio',
            field=models.CharField(max_length=511, help_text="This person's professional background.", default='', blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='person',
            name='title',
            field=models.CharField(max_length=255, help_text="This person's role within the IETF.", default='', blank=True),
            preserve_default=False,
        ),
    ]
