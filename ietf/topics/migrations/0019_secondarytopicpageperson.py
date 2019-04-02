# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('datatracker', '0019_role_group'),
        ('topics', '0018_auto_20160620_1524'),
    ]

    operations = [
        migrations.CreateModel(
            name='SecondaryTopicPagePerson',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('page', modelcluster.fields.ParentalKey(to='topics.SecondaryTopicPage', related_name='people')),
                ('person', models.ForeignKey(to='datatracker.Person', related_name='+')),
            ],
        ),
    ]
