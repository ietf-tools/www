# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import modelcluster.fields
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0021_auto_20160127_1534'),
        ('blog', '0013_auto_20151209_1517'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPageAuthor',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('author', models.ForeignKey(related_name='+', to='snippets.Person')),
            ],
        ),
        migrations.RemoveField(
            model_name='blogpage',
            name='author',
        ),
        migrations.AddField(
            model_name='blogpageauthor',
            name='page',
            field=modelcluster.fields.ParentalKey(related_name='authors', to='blog.BlogPage'),
        ),
        migrations.AddField(
            model_name='blogpageauthor',
            name='role',
            field=models.ForeignKey(related_name='+', help_text="Override the person's current role for this blog post.", null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL, to='snippets.Role'),
        ),
    ]
