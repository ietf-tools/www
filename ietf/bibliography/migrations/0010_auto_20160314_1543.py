# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailredirects', '0005_capitalizeverbose'),
        ('wagtailsearchpromotions', '0002_capitalizeverbose'),
        ('wagtailcore', '0024_alter_page_content_type_on_delete_behaviour'),
        ('wagtailforms', '0003_capitalizeverbose'),
        ('bibliography', '0009_auto_20151027_1627'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bibliographytestpage',
            name='page_ptr',
        ),
        migrations.DeleteModel(
            name='BibliographyTestPage',
        ),
    ]
