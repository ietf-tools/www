# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0008_auto_20150814_1641'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mailinglistsignup',
            name='signup_email',
        ),
        migrations.AddField(
            model_name='mailinglistsignup',
            name='sign_up',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
