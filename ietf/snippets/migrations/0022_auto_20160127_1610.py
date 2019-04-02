# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0021_auto_20160127_1534'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='role',
        ),
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(help_text='A role within the IETF.', max_length=255),
        ),
    ]
