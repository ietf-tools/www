# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_auto_20160315_1523'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpageauthor',
            name='author',
        ),
        migrations.RemoveField(
            model_name='blogpageauthor',
            name='page',
        ),
        migrations.RemoveField(
            model_name='blogpageauthor',
            name='role',
        ),
        migrations.DeleteModel(
            name='BlogPageAuthor',
        ),
    ]
