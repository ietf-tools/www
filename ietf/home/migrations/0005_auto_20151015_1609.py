# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_homepage_main_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='internet_drafts_section_body',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='request_for_comments_section_body',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='working_groups_section_body',
            field=models.CharField(max_length=500),
        ),
    ]
