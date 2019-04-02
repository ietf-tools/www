# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0019_secondarytopicpageperson'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='primarytopicpage',
            options={'verbose_name': 'Topic Page'},
        ),
        migrations.AlterModelOptions(
            name='secondarytopicpage',
            options={'verbose_name': 'Area Page'},
        ),
        migrations.AlterModelOptions(
            name='topicindexpage',
            options={'verbose_name': 'Topic Page List'},
        ),
    ]
