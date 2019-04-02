# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import modelcluster.fields
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0011_auto_20150817_1726'),
        ('datatracker', '0014_auto_20150814_1641'),
        ('wagtaildocs', '0003_add_verbose_names'),
        ('wagtailcore', '0019_verbose_names_cleanup'),
        ('home', '0002_create_homepage'),
    ]

    operations = [
        migrations.CreateModel(
            name='InternetDraftsSectionLinks',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('link_external', models.URLField(verbose_name='External link', blank=True)),
                ('title', models.CharField(help_text='Link title', max_length=255)),
                ('link_document', models.ForeignKey(to='wagtaildocs.Document', related_name='+', null=True, blank=True)),
                ('link_page', models.ForeignKey(to='wagtailcore.Page', related_name='+', null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RequestForCommentsSectionLinks',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('link_external', models.URLField(verbose_name='External link', blank=True)),
                ('title', models.CharField(help_text='Link title', max_length=255)),
                ('link_document', models.ForeignKey(to='wagtaildocs.Document', related_name='+', null=True, blank=True)),
                ('link_page', models.ForeignKey(to='wagtailcore.Page', related_name='+', null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WorkingGroupsSectionLinks',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('link_external', models.URLField(verbose_name='External link', blank=True)),
                ('title', models.CharField(help_text='Link title', max_length=255)),
                ('link_document', models.ForeignKey(to='wagtaildocs.Document', related_name='+', null=True, blank=True)),
                ('link_page', models.ForeignKey(to='wagtailcore.Page', related_name='+', null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='homepage',
            name='button_link',
            field=models.ForeignKey(to='wagtailcore.Page', on_delete=django.db.models.deletion.SET_NULL, related_name='+', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='button_text',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='call_to_action',
            field=models.ForeignKey(to='snippets.CallToAction', on_delete=django.db.models.deletion.SET_NULL, related_name='+', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='heading',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='homepage',
            name='highlighted_internet_draft',
            field=models.ForeignKey(to='datatracker.InternetDraft', on_delete=django.db.models.deletion.SET_NULL, related_name='+', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='highlighted_request_for_comment',
            field=models.ForeignKey(to='datatracker.RFC', on_delete=django.db.models.deletion.SET_NULL, related_name='+', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='highlighted_working_group',
            field=models.ForeignKey(to='datatracker.WorkingGroup', on_delete=django.db.models.deletion.SET_NULL, related_name='+', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='internet_drafts_section_body',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='homepage',
            name='introduction',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='homepage',
            name='request_for_comments_section_body',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='homepage',
            name='working_groups_section_body',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='workinggroupssectionlinks',
            name='page',
            field=modelcluster.fields.ParentalKey(related_name='working_groups_section_links', to='home.HomePage'),
        ),
        migrations.AddField(
            model_name='requestforcommentssectionlinks',
            name='page',
            field=modelcluster.fields.ParentalKey(related_name='request_for_comments_section_links', to='home.HomePage'),
        ),
        migrations.AddField(
            model_name='internetdraftssectionlinks',
            name='page',
            field=modelcluster.fields.ParentalKey(related_name='internet_drafts_section_links', to='home.HomePage'),
        ),
    ]
