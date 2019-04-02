# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0013_auto_20151028_1238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='bio',
            field=models.CharField(max_length=511, help_text="This person's professional background.", blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='image',
            field=models.ForeignKey(null=True, help_text='A photograph of this person.', blank=True, to='wagtailimages.Image', related_name='+'),
        ),
        migrations.AlterField(
            model_name='person',
            name='title',
            field=models.CharField(max_length=255, help_text="This person's role within the IETF.", blank=True, null=True),
        ),
    ]
