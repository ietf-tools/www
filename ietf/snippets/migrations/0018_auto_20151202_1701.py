# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0017_sponsor_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='glossaryitem',
            name='body',
            field=wagtail.core.fields.RichTextField(help_text='Explanation of the glossary term.'),
        ),
    ]
