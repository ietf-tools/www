# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0024_alter_page_content_type_on_delete_behaviour'),
        ('wagtaildocs', '0005_alter_uploaded_by_user_on_delete_action'),
        ('utils', '0004_socialmediasettings'),
    ]

    operations = [
        migrations.CreateModel(
            name='FooterLinkItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('sort_order', models.IntegerField(null=True, blank=True, editable=False)),
                ('link_external', models.URLField(verbose_name='External link', blank=True)),
                ('link_document', models.ForeignKey(related_name='+', to='wagtaildocs.Document', null=True, blank=True)),
                ('link_page', models.ForeignKey(related_name='+', to='wagtailcore.Page', null=True, blank=True)),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FooterLinks',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('site', models.OneToOneField(editable=False, to='wagtailcore.Site')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='footerlinkitem',
            name='model',
            field=modelcluster.fields.ParentalKey(related_name='footer_link_items', to='utils.FooterLinks'),
        ),
    ]
