# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0024_alter_page_content_type_on_delete_behaviour'),
        ('images', '0002_auto_20160314_1710'),
        ('utils', '0003_auto_20160908_1202'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialMediaSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('twitter_handle', models.CharField(blank='True', max_length=255, help_text='Your Twitter username without the @, e.g. flickr')),
                ('facebook_app_id', models.CharField(blank='True', max_length=255, help_text='Your Facebook app id')),
                ('default_sharing_text', models.CharField(blank='True', max_length=255, help_text='Default sharing text to use if social text has not been set on a page.')),
                ('site_name', models.CharField(blank='True', max_length=255, help_text='Site name, used by facebook open graph.', default='ietf')),
                ('default_sharing_image', models.ForeignKey(related_name='+', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, help_text='Default sharing image to use if social image has not been set on a page.', to='images.IETFImage')),
                ('site', models.OneToOneField(to='wagtailcore.Site', editable=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
