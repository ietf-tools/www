# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bibliography', '0006_bibliographyitem_content_identifier'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bibliographytestpage',
            name='prepared_page_content',
        ),
    ]
