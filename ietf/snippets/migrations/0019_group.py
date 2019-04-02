# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.search.index
import ietf.snippets.models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0008_image_created_at_index'),
        ('snippets', '0018_auto_20151202_1701'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=255, help_text="This group's name.")),
                ('role', models.CharField(blank=True, max_length=255, help_text="This group's role within the IETF.")),
                ('summary', models.CharField(blank=True, max_length=511, help_text='More information about this group.')),
                ('email', models.EmailField(blank=True, max_length=254, help_text="This group's email address.")),
                ('image', models.ForeignKey(null=True, to='wagtailimages.Image', related_name='+', blank=True, help_text='An image to represent this group.')),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model, wagtail.search.index.Indexed, ietf.snippets.models.RenderableSnippetMixin),
        ),
    ]
