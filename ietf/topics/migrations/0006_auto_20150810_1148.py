# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0005_auto_20150807_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='primarytosecondaryrelationship',
            name='secondary_topic',
            field=models.ForeignKey(related_name='primary_topics', to='topics.SecondaryTopicPage'),
        ),
    ]
