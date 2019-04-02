# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import modelcluster.fields
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0006_add_verbose_names'),
        ('wagtailcore', '0001_squashed_0016_change_page_url_path_to_text_field'),
        ('wagtaildocs', '0003_add_verbose_names'),
    ]

    operations = [
        migrations.CreateModel(
            name='GlossaryPage',
            fields=[
                ('page_ptr', models.OneToOneField(primary_key=True, to='wagtailcore.Page', serialize=False, auto_created=True, parent_link=True)),
                ('social_text', models.CharField(blank=True, help_text='Description of this page as it should appear when shared on social networks, or in Google results', max_length=255)),
                ('introduction', models.CharField(max_length=511)),
                ('feed_image', models.ForeignKey(related_name='+', null=True, help_text='This image will be used in listings and indexes across the site, if no feed image is added, the social image will be used.', to='wagtailimages.Image', blank=True, on_delete=django.db.models.deletion.SET_NULL)),
                ('social_image', models.ForeignKey(related_name='+', null=True, help_text="Image to appear alongside 'social text', particularly for sharing on social networks", to='wagtailimages.Image', blank=True, on_delete=django.db.models.deletion.SET_NULL)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page', models.Model),
        ),
        migrations.CreateModel(
            name='GlossaryPageRelatedLink',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('sort_order', models.IntegerField(null=True, editable=False, blank=True)),
                ('link_external', models.URLField(verbose_name='External link', blank=True)),
                ('title', models.CharField(help_text='Link title', max_length=255)),
                ('link_document', models.ForeignKey(related_name='+', null=True, to='wagtaildocs.Document', blank=True)),
                ('link_page', models.ForeignKey(related_name='+', null=True, to='wagtailcore.Page', blank=True)),
                ('page', modelcluster.fields.ParentalKey(related_name='related_links', to='glossary.GlossaryPage')),
            ],
            options={
                'abstract': False,
                'ordering': ['sort_order'],
            },
        ),
    ]
