# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ietf.datatracker.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=511)),
            ],
            bases=(ietf.datatracker.models.DatatrackerMixin, models.Model),
        ),
    ]
