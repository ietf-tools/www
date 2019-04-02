# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

from wagtail.images.utils import get_fill_filter_spec_migrations


forward, reverse = get_fill_filter_spec_migrations('images', 'IETFRendition')


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0005_wagtail_1_7'),
    ]

    operations = [
        migrations.RunPython(forward, reverse),
    ]
