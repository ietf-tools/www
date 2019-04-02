# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bibliography', '0010_auto_20160314_1543'),
    ]

    operations = [
        migrations.AddField(
            model_name='bibliographyitem',
            name='content_long_title',
            field=models.CharField(blank=True, max_length=127),
        ),
    ]
