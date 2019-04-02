# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import modelcluster.fields
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0001_squashed_0016_change_page_url_path_to_text_field'),
    ]

    operations = [
        migrations.CreateModel(
            name='FormField',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('sort_order', models.IntegerField(null=True, blank=True, editable=False)),
                ('label', models.CharField(verbose_name='Label', max_length=255, help_text='The label of the form field')),
                ('field_type', models.CharField(verbose_name='Field type', max_length=16, choices=[('singleline', 'Single line text'), ('multiline', 'Multi-line text'), ('email', 'Email'), ('number', 'Number'), ('url', 'URL'), ('checkbox', 'Checkbox'), ('checkboxes', 'Checkboxes'), ('dropdown', 'Drop down'), ('radio', 'Radio buttons'), ('date', 'Date'), ('datetime', 'Date/time')])),
                ('required', models.BooleanField(verbose_name='Required', default=True)),
                ('choices', models.CharField(verbose_name='Choices', max_length=512, blank=True, help_text='Comma separated list of choices. Only applicable in checkboxes, radio and dropdown.')),
                ('default_value', models.CharField(verbose_name='Default value', max_length=255, blank=True, help_text='Default value. Comma separated values supported for checkboxes.')),
                ('help_text', models.CharField(verbose_name='Help text', max_length=255, blank=True)),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FormPage',
            fields=[
                ('page_ptr', models.OneToOneField(serialize=False, auto_created=True, to='wagtailcore.Page', parent_link=True, primary_key=True)),
                ('to_address', models.CharField(verbose_name='To address', max_length=255, blank=True, help_text='Optional - form submissions will be emailed to this address')),
                ('from_address', models.CharField(verbose_name='From address', max_length=255, blank=True)),
                ('subject', models.CharField(verbose_name='Subject', max_length=255, blank=True)),
                ('intro', wagtail.core.fields.RichTextField(blank=True)),
                ('thank_you_text', wagtail.core.fields.RichTextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.AddField(
            model_name='formfield',
            name='page',
            field=modelcluster.fields.ParentalKey(to='forms.FormPage', related_name='form_fields'),
        ),
    ]
