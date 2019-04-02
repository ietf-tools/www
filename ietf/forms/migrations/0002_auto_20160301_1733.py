# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formfield',
            name='choices',
            field=models.CharField(max_length=512, help_text='Comma separated list of choices. Only applicable in checkboxes, radio and dropdown.', verbose_name='choices', blank=True),
        ),
        migrations.AlterField(
            model_name='formfield',
            name='default_value',
            field=models.CharField(max_length=255, help_text='Default value. Comma separated values supported for checkboxes.', verbose_name='default value', blank=True),
        ),
        migrations.AlterField(
            model_name='formfield',
            name='field_type',
            field=models.CharField(max_length=16, verbose_name='field type', choices=[('singleline', 'Single line text'), ('multiline', 'Multi-line text'), ('email', 'Email'), ('number', 'Number'), ('url', 'URL'), ('checkbox', 'Checkbox'), ('checkboxes', 'Checkboxes'), ('dropdown', 'Drop down'), ('radio', 'Radio buttons'), ('date', 'Date'), ('datetime', 'Date/time')]),
        ),
        migrations.AlterField(
            model_name='formfield',
            name='help_text',
            field=models.CharField(max_length=255, verbose_name='help text', blank=True),
        ),
        migrations.AlterField(
            model_name='formfield',
            name='label',
            field=models.CharField(max_length=255, help_text='The label of the form field', verbose_name='label'),
        ),
        migrations.AlterField(
            model_name='formfield',
            name='required',
            field=models.BooleanField(verbose_name='required', default=True),
        ),
        migrations.AlterField(
            model_name='formpage',
            name='from_address',
            field=models.CharField(max_length=255, verbose_name='from address', blank=True),
        ),
        migrations.AlterField(
            model_name='formpage',
            name='subject',
            field=models.CharField(max_length=255, verbose_name='subject', blank=True),
        ),
        migrations.AlterField(
            model_name='formpage',
            name='to_address',
            field=models.CharField(max_length=255, help_text='Optional - form submissions will be emailed to this address', verbose_name='to address', blank=True),
        ),
    ]
