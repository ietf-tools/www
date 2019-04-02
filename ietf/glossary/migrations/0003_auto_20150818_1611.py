# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0011_auto_20150817_1726'),
        ('glossary', '0002_auto_20150818_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='glossarypage',
            name='call_to_action',
            field=models.ForeignKey(null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL, to='snippets.CallToAction', blank=True),
        ),
        migrations.AddField(
            model_name='glossarypage',
            name='mailing_list_signup',
            field=models.ForeignKey(null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL, to='snippets.MailingListSignup', blank=True),
        ),
    ]
