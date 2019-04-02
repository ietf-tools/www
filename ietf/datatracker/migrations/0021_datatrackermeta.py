# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('datatracker', '0020_auto_20160620_1652'),
    ]

    operations = [
        migrations.CreateModel(
            name='DatatrackerMeta',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('last_page_seen', models.CharField(blank=True, max_length=511)),
                ('last_updated', models.DateTimeField(null=True, blank=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
        ),
    ]
