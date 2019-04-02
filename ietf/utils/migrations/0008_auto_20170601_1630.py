# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0024_alter_page_content_type_on_delete_behaviour'),
        ('utils', '0007_auto_20170601_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='secondarymenu',
            name='tools_page',
            field=models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL, to='wagtailcore.Page'),
        ),
        migrations.AlterField(
            model_name='toolsmenuitem',
            name='model',
            field=modelcluster.fields.ParentalKey(related_name='tools_menu_items', to='utils.SecondaryMenu'),
        ),
    ]
