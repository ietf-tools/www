# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0002_moremenuitem_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='moremenuitem',
            name='text',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='moremenuitem',
            name='page',
            field=models.ForeignKey(null=True, blank=True, to='wagtailcore.Page', related_name='+', on_delete=django.db.models.deletion.SET_NULL),
        ),
    ]
