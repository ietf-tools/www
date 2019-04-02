# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0006_auto_20150810_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='secondarytopicpage',
            name='introduction',
            field=models.CharField(help_text='Enter the introduction to display on the page, you can use only 255 characters.', max_length=255),
        ),
        migrations.AlterField(
            model_name='topicindexpage',
            name='introduction',
            field=models.CharField(help_text='Enter the introduction to display on the page, you can use only 255 characters.', max_length=255),
        ),
    ]
