# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0011_auto_20150817_1726'),
        ('topics', '0007_auto_20150818_1100'),
    ]

    operations = [
        migrations.AddField(
            model_name='secondarytopicpage',
            name='call_to_action',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.SET_NULL, null=True, to='snippets.CallToAction', related_name='+'),
        ),
        migrations.AddField(
            model_name='secondarytopicpage',
            name='mailing_list_signup',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.SET_NULL, null=True, to='snippets.MailingListSignup', related_name='+'),
        ),
    ]
