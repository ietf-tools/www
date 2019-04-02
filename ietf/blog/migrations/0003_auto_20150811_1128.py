# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0005_primarytopic_secondarytopic'),
        ('blog', '0002_auto_20150811_1128'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpagesecondarytopic',
            name='topic',
            field=models.ForeignKey(to='snippets.SecondaryTopic', related_name='+'),
        ),
        migrations.AddField(
            model_name='blogpageprimarytopic',
            name='page',
            field=modelcluster.fields.ParentalKey(to='blog.BlogPage', related_name='primary_topics'),
        ),
        migrations.AddField(
            model_name='blogpageprimarytopic',
            name='topic',
            field=models.ForeignKey(to='snippets.PrimaryTopic', related_name='+'),
        ),
    ]
