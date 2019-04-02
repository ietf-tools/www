# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0006_footerlinkitem_title'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MoreMenuItem',
            new_name='ToolsMenuItem',
        ),
    ]
