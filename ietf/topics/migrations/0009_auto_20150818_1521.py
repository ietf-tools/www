# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import modelcluster.fields
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0001_squashed_0016_change_page_url_path_to_text_field'),
        ('wagtaildocs', '0003_add_verbose_names'),
        ('snippets', '0011_auto_20150817_1726'),
        ('topics', '0008_auto_20150818_1507'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrimaryTopicPageRelatedLink',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('sort_order', models.IntegerField(null=True, editable=False, blank=True)),
                ('link_external', models.URLField(verbose_name='External link', blank=True)),
                ('title', models.CharField(help_text='Link title', max_length=255)),
                ('link_document', models.ForeignKey(blank=True, null=True, to='wagtaildocs.Document', related_name='+')),
                ('link_page', models.ForeignKey(blank=True, null=True, to='wagtailcore.Page', related_name='+')),
            ],
            options={
                'abstract': False,
                'ordering': ['sort_order'],
            },
        ),
        migrations.CreateModel(
            name='SecondaryPageRelatedLink',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('sort_order', models.IntegerField(null=True, editable=False, blank=True)),
                ('link_external', models.URLField(verbose_name='External link', blank=True)),
                ('title', models.CharField(help_text='Link title', max_length=255)),
                ('link_document', models.ForeignKey(blank=True, null=True, to='wagtaildocs.Document', related_name='+')),
                ('link_page', models.ForeignKey(blank=True, null=True, to='wagtailcore.Page', related_name='+')),
                ('page', modelcluster.fields.ParentalKey(to='topics.SecondaryTopicPage', related_name='related_links')),
            ],
            options={
                'abstract': False,
                'ordering': ['sort_order'],
            },
        ),
        migrations.AddField(
            model_name='primarytopicpage',
            name='call_to_action',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.SET_NULL, null=True, to='snippets.CallToAction', related_name='+'),
        ),
        migrations.AddField(
            model_name='primarytopicpage',
            name='mailing_list_signup',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.SET_NULL, null=True, to='snippets.MailingListSignup', related_name='+'),
        ),
        migrations.AddField(
            model_name='primarytopicpagerelatedlink',
            name='page',
            field=modelcluster.fields.ParentalKey(to='topics.PrimaryTopicPage', related_name='related_links'),
        ),
    ]
