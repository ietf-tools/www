# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0004_auto_20150807_1230'),
        ('topics', '0002_auto_20150805_1350'),
    ]

    operations = [
        migrations.CreateModel(
            name='SecondaryTopicPagePerson',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('page', modelcluster.fields.ParentalKey(related_name='people', to='topics.SecondaryTopicPage')),
                ('person', models.ForeignKey(related_name='+', to='snippets.Person')),
            ],
        ),
    ]
