# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0016_auto_20160315_1523'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='secondarytopicpageperson',
            name='person',
        ),
    ]
