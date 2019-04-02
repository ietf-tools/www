# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0006_add_verbose_names'),
        ('snippets', '0002_delete_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('bio', models.CharField(max_length=511)),
                ('email', models.EmailField(max_length=254)),
                ('image', models.ForeignKey(related_name='+', to='wagtailimages.Image')),
            ],
            options={
                'verbose_name': 'People',
                'ordering': ['name'],
            },
        ),
    ]
