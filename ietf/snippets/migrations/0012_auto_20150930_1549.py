# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0011_auto_20150817_1726'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='calltoaction',
            options={'verbose_name_plural': 'Calls to action', 'ordering': ['title']},
        ),
        migrations.AlterModelOptions(
            name='glossaryitem',
            options={'ordering': ['title']},
        ),
        migrations.AlterModelOptions(
            name='mailinglistsignup',
            options={'ordering': ['title']},
        ),
        migrations.AlterModelOptions(
            name='primarytopic',
            options={'ordering': ['title']},
        ),
        migrations.AlterModelOptions(
            name='secondarytopic',
            options={'ordering': ['title']},
        ),
        migrations.AlterModelOptions(
            name='sponsor',
            options={'ordering': ['title']},
        ),
    ]
