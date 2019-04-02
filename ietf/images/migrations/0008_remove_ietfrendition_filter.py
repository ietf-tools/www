# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0007_wagtail_1_8'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ietfrendition',
            name='filter',
        ),
    ]
