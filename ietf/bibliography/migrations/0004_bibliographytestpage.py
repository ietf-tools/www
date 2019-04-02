# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0001_squashed_0016_change_page_url_path_to_text_field'),
        ('bibliography', '0003_bibliographyitem_page'),
    ]

    operations = [
        migrations.CreateModel(
            name='BibliographyTestPage',
            fields=[
                ('page_ptr', models.OneToOneField(serialize=False, primary_key=True, auto_created=True, parent_link=True, to='wagtailcore.Page')),
                ('prepared_page_content', models.TextField(null=True, blank=True, help_text='The prepared page content after bibliography styling has been applied. Auto-generated on each save.')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page', models.Model),
        ),
    ]
