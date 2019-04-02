# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0001_squashed_0016_change_page_url_path_to_text_field'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrimaryTopicPage',
            fields=[
                ('page_ptr', models.OneToOneField(serialize=False, auto_created=True, to='wagtailcore.Page', parent_link=True, primary_key=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='SecondaryTopicPage',
            fields=[
                ('page_ptr', models.OneToOneField(serialize=False, auto_created=True, to='wagtailcore.Page', parent_link=True, primary_key=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='TopicIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(serialize=False, auto_created=True, to='wagtailcore.Page', parent_link=True, primary_key=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
