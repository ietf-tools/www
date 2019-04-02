# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.search.index


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0006_sponsor'),
    ]

    operations = [
        migrations.CreateModel(
            name='GlossaryItem',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('body', models.TextField()),
            ],
            bases=(wagtail.search.index.Indexed, models.Model),
        ),
    ]
