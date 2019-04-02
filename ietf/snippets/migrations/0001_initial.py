# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtaildocs', '0003_add_verbose_names'),
        ('wagtailcore', '0001_squashed_0016_change_page_url_path_to_text_field'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='CallToAction',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('link_external', models.URLField(verbose_name='External link', blank=True)),
                ('title', models.CharField(max_length=255, help_text='Link title')),
                ('heading', models.CharField(max_length=255, help_text='The text that appears above the link.')),
                ('link_document', models.ForeignKey(null=True, related_name='+', blank=True, to='wagtaildocs.Document')),
                ('link_page', models.ForeignKey(null=True, related_name='+', blank=True, to='wagtailcore.Page')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
