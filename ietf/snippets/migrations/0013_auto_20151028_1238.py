# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0012_auto_20150930_1549'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='glossaryitem',
            options={'ordering': ['title'], 'verbose_name': 'Glossary Item'},
        ),
    ]
