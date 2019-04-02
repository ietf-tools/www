# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('datatracker', '0020_auto_20160620_1652'),
        ('snippets', '0024_auto_20160525_1405'),
        ('blog', '0016_auto_20160620_1652'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPageAuthor',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('author', models.ForeignKey(related_name='+', to='datatracker.Person')),
                ('page', modelcluster.fields.ParentalKey(related_name='authors', to='blog.BlogPage')),
                ('role', models.ForeignKey(related_name='+', null=True, help_text="Override the person's current role for this blog post.", on_delete=django.db.models.deletion.SET_NULL, blank=True, to='snippets.Role')),
            ],
        ),
    ]
