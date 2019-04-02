# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0011_auto_20150817_1726'),
        ('standard', '0005_standardpagefaqitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='standardpage',
            name='mailing_list_signup',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', null=True, to='snippets.MailingListSignup'),
        ),
    ]
