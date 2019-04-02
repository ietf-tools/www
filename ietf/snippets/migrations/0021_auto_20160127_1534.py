# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.search.index


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0020_remove_person_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(help_text="A person's role within the IETF.", max_length=255)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model, wagtail.search.index.Indexed),
        ),
        migrations.AddField(
            model_name='person',
            name='role',
            field=models.ForeignKey(to='snippets.Role', related_name='+', blank=True, null=True, help_text="This person's role within the IETF."),
        ),
    ]
