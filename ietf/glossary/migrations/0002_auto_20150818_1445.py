# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('glossary', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='glossarypage',
            name='introduction',
            field=models.CharField(max_length=511, help_text='The page introduction text. You can only use 511 characters.'),
        ),
    ]
