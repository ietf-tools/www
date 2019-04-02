# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datatracker', '0014_auto_20150814_1641'),
        ('snippets', '0007_glossaryitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='MailingListSignup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('blurb', models.CharField(blank=True, max_length=255)),
                ('button_text', models.CharField(max_length=255)),
                ('signup_email', models.EmailField(blank=True, max_length=254)),
                ('working_group', models.ForeignKey(to='datatracker.WorkingGroup', blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+')),
            ],
        ),
        migrations.AlterModelOptions(
            name='calltoaction',
            options={'verbose_name_plural': 'Calls To Action'},
        ),
        migrations.RemoveField(
            model_name='calltoaction',
            name='heading',
        ),
        migrations.AddField(
            model_name='calltoaction',
            name='blurb',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='calltoaction',
            name='button_text',
            field=models.CharField(max_length=255, default=''),
            preserve_default=False,
        ),
    ]
