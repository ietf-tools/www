# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0019_verbose_names_cleanup'),
        ('snippets', '0011_auto_20150817_1726'),
    ]

    operations = [
        migrations.CreateModel(
            name='MoreMenuItem',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NewsAndBlogsMenuItem',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SecondaryMenu',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('contact_page', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, related_name='+', to='wagtailcore.Page')),
                ('site', models.OneToOneField(to='wagtailcore.Site', editable=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='newsandblogsmenuitem',
            name='model',
            field=modelcluster.fields.ParentalKey(related_name='news_and_blogs_menu_items', to='utils.SecondaryMenu'),
        ),
        migrations.AddField(
            model_name='newsandblogsmenuitem',
            name='snippet',
            field=models.ForeignKey(related_name='+', to='snippets.PrimaryTopic'),
        ),
        migrations.AddField(
            model_name='moremenuitem',
            name='model',
            field=modelcluster.fields.ParentalKey(related_name='more_menu_items', to='utils.SecondaryMenu'),
        ),
        migrations.AddField(
            model_name='moremenuitem',
            name='page',
            field=models.ForeignKey(related_name='+', to='wagtailcore.Page'),
        ),
    ]
