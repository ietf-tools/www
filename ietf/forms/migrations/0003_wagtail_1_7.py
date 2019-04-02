# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0002_auto_20160301_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formfield',
            name='choices',
            field=models.TextField(help_text='Comma separated list of choices. Only applicable in checkboxes, radio and dropdown.', verbose_name='choices', blank=True),
        ),
        migrations.AlterField(
            model_name='formpage',
            name='to_address',
            field=models.CharField(help_text='Optional - form submissions will be emailed to these addresses. Separate multiple addresses by comma.', max_length=255, verbose_name='to address', blank=True),
        ),
    ]
