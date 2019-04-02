# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0022_auto_20160127_1610'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='role',
            field=models.ForeignKey(blank=True, help_text="This group's role within the IETF.", related_name='+', to='snippets.Role', null=True),
        ),
    ]
