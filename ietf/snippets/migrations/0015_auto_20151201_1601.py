# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0014_auto_20151201_1553'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='glossaryitem',
            options={'ordering': ['title'], 'verbose_name': 'Glossary item'},
        ),
    ]
