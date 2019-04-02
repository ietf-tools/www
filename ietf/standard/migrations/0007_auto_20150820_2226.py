# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('datatracker', '0014_auto_20150814_1641'),
        ('standard', '0006_standardpage_mailing_list_signup'),
    ]

    operations = [
        migrations.CreateModel(
            name='StandardPageArea',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort_order', models.IntegerField(editable=False, null=True, blank=True)),
                ('area', models.ForeignKey(related_name='standard_pages', to='datatracker.Area')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StandardPageCharter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort_order', models.IntegerField(editable=False, null=True, blank=True)),
                ('charter', models.ForeignKey(related_name='standard_pages', to='datatracker.Charter')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StandardPageInternetDraft',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort_order', models.IntegerField(editable=False, null=True, blank=True)),
                ('internet_draft', models.ForeignKey(related_name='standard_pages', to='datatracker.InternetDraft')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StandardPageRFC',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort_order', models.IntegerField(editable=False, null=True, blank=True)),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StandardPageWorkingGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort_order', models.IntegerField(editable=False, null=True, blank=True)),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='standardpage',
            name='area_uri',
        ),
        migrations.RemoveField(
            model_name='standardpage',
            name='charter_uri',
        ),
        migrations.RemoveField(
            model_name='standardpage',
            name='internet_draft_uri',
        ),
        migrations.RemoveField(
            model_name='standardpage',
            name='rfc_uri',
        ),
        migrations.RemoveField(
            model_name='standardpage',
            name='working_group_uri',
        ),
        migrations.AddField(
            model_name='standardpageworkinggroup',
            name='page',
            field=modelcluster.fields.ParentalKey(related_name='working_groups', to='standard.StandardPage'),
        ),
        migrations.AddField(
            model_name='standardpageworkinggroup',
            name='working_group',
            field=models.ForeignKey(related_name='standard_pages', to='datatracker.WorkingGroup'),
        ),
        migrations.AddField(
            model_name='standardpagerfc',
            name='page',
            field=modelcluster.fields.ParentalKey(related_name='rfcs', to='standard.StandardPage'),
        ),
        migrations.AddField(
            model_name='standardpagerfc',
            name='rfc',
            field=models.ForeignKey(related_name='standard_pages', to='datatracker.RFC'),
        ),
        migrations.AddField(
            model_name='standardpageinternetdraft',
            name='page',
            field=modelcluster.fields.ParentalKey(related_name='internet_drafts', to='standard.StandardPage'),
        ),
        migrations.AddField(
            model_name='standardpagecharter',
            name='page',
            field=modelcluster.fields.ParentalKey(related_name='charters', to='standard.StandardPage'),
        ),
        migrations.AddField(
            model_name='standardpagearea',
            name='page',
            field=modelcluster.fields.ParentalKey(related_name='areas', to='standard.StandardPage'),
        ),
    ]
