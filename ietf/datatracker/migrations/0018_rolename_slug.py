# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datatracker', '0017_email_person_role_rolename'),
    ]

    operations = [
        migrations.AddField(
            model_name='rolename',
            name='slug',
            field=models.CharField(max_length=511, default=''),
            preserve_default=False,
        ),
    ]
