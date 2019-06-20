# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0024_auto_20160525_1405'),
        ('topics', '0017_remove_secondarytopicpageperson_person'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='image',
        ),
        migrations.RemoveField(
            model_name='person',
            name='role',
        ),
        migrations.DeleteModel(
            name='Person',
        ),
    ]
