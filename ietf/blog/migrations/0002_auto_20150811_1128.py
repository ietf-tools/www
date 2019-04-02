# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import wagtail.core.fields
import wagtail.images.blocks
import modelcluster.fields
import wagtail.core.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0006_add_verbose_names'),
        ('snippets', '0004_auto_20150807_1230'),
        ('wagtailcore', '0001_squashed_0016_change_page_url_path_to_text_field'),
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(primary_key=True, auto_created=True, serialize=False, to='wagtailcore.Page', parent_link=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='BlogPagePrimaryTopic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
            ],
        ),
        migrations.CreateModel(
            name='BlogPageSecondaryTopic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
            ],
        ),
        migrations.AddField(
            model_name='blogpage',
            name='author',
            field=models.ForeignKey(default=1, to='snippets.Person', related_name='+', on_delete=django.db.models.deletion.PROTECT),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='blogpage',
            name='body',
            field=wagtail.core.fields.StreamField((('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())), default=[]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='blogpage',
            name='date_published',
            field=models.DateField(blank=True, null=True, help_text='Use this field to override the date that the blog post appears to have been published.'),
        ),
        migrations.AddField(
            model_name='blogpage',
            name='feed_image',
            field=models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL, help_text='This image will be used in listings and indexes across the site, if no feed image is added, the social image will be used.', to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='blogpage',
            name='introduction',
            field=models.CharField(default='', max_length=511),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='blogpage',
            name='social_image',
            field=models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL, help_text="Image to appear alongside 'social text', particularly for sharing on social networks", to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='blogpage',
            name='social_text',
            field=models.CharField(blank=True, max_length=255, help_text='Description of this page as it should appear when shared on social networks, or in Google results'),
        ),
        migrations.AddField(
            model_name='blogpagesecondarytopic',
            name='page',
            field=modelcluster.fields.ParentalKey(to='blog.BlogPage', related_name='secondary_topics'),
        ),
    ]
