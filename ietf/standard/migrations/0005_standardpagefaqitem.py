# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('standard', '0004_standardpagefeedrelatedlink'),
    ]

    operations = [
        migrations.CreateModel(
            name='StandardPageFAQItem',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('sort_order', models.IntegerField(null=True, blank=True, editable=False)),
                ('question', models.TextField()),
                ('answer', models.TextField()),
                ('page', modelcluster.fields.ParentalKey(related_name='faq_items', to='standard.StandardPage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
