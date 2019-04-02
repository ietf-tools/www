# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.images.models
import taggit.managers
from django.conf import settings
import django.db.models.deletion
import wagtail.search.index

class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('wagtailimages', '0010_change_on_delete_behaviour'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='IETFImage',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('file', models.ImageField(height_field='height', width_field='width', upload_to=wagtail.images.models.get_upload_to, verbose_name='file')),
                ('width', models.IntegerField(editable=False, verbose_name='width')),
                ('height', models.IntegerField(editable=False, verbose_name='height')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at', db_index=True)),
                ('focal_point_x', models.PositiveIntegerField(blank=True, null=True)),
                ('focal_point_y', models.PositiveIntegerField(blank=True, null=True)),
                ('focal_point_width', models.PositiveIntegerField(blank=True, null=True)),
                ('focal_point_height', models.PositiveIntegerField(blank=True, null=True)),
                ('file_size', models.PositiveIntegerField(editable=False, null=True)),
                ('caption', models.CharField(max_length=255, blank=True, null=True)),
                ('tags', taggit.managers.TaggableManager(blank=True, verbose_name='tags', through='taggit.TaggedItem', to='taggit.Tag', help_text=None)),
                ('uploaded_by_user', models.ForeignKey(verbose_name='uploaded by user', blank=True, null=True, to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.SET_NULL, editable=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, wagtail.search.index.Indexed),
        ),
        migrations.CreateModel(
            name='IETFRendition',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('file', models.ImageField(height_field='height', width_field='width', upload_to='images')),
                ('width', models.IntegerField(editable=False)),
                ('height', models.IntegerField(editable=False)),
                ('focal_point_key', models.CharField(editable=False, max_length=255, default='', blank=True)),
                ('filter', models.ForeignKey(related_name='+', to='wagtailimages.Filter')),
                ('image', models.ForeignKey(related_name='renditions', to='images.IETFImage')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='ietfrendition',
            unique_together=set([('image', 'filter', 'focal_point_key')]),
        ),
    ]
