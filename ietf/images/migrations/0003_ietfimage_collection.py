# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.core.models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0028_merge'),
        ('images', '0002_auto_20160314_1710'),
    ]

    operations = [
        migrations.AddField(
            model_name='ietfimage',
            name='collection',
            field=models.ForeignKey(to='wagtailcore.Collection', default=wagtail.core.models.get_root_collection_id, verbose_name='collection', related_name='+'),
        ),
    ]
