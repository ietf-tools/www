# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0001_squashed_0016_change_page_url_path_to_text_field'),
        ('wagtaildocs', '0003_add_verbose_names'),
        ('standard', '0003_auto_20150812_1616'),
    ]

    operations = [
        migrations.CreateModel(
            name='StandardPageFeedRelatedLink',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('sort_order', models.IntegerField(null=True, blank=True, editable=False)),
                ('link_external', models.URLField(blank=True, verbose_name='External link')),
                ('title', models.CharField(max_length=255, help_text='Link title')),
                ('link_document', models.ForeignKey(null=True, blank=True, to='wagtaildocs.Document', related_name='+')),
                ('link_page', models.ForeignKey(null=True, blank=True, to='wagtailcore.Page', related_name='+')),
                ('page', modelcluster.fields.ParentalKey(to='standard.StandardPage', related_name='feed_related_links')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
