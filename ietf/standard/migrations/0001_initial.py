# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.core.fields
import wagtail.images.blocks
import modelcluster.fields
import django.db.models.deletion
import wagtail.core.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtaildocs', '0003_add_verbose_names'),
        ('snippets', '0001_initial'),
        ('wagtailcore', '0001_squashed_0016_change_page_url_path_to_text_field'),
        ('wagtailimages', '0006_add_verbose_names'),
    ]

    operations = [
        migrations.CreateModel(
            name='StandardIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(serialize=False, auto_created=True, to='wagtailcore.Page', parent_link=True, primary_key=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='StandardPage',
            fields=[
                ('page_ptr', models.OneToOneField(serialize=False, auto_created=True, to='wagtailcore.Page', parent_link=True, primary_key=True)),
                ('social_text', models.CharField(max_length=255, blank=True, help_text='Description of this page as it should appear when shared on social networks, or in Google results')),
                ('introduction', models.CharField(max_length=255, help_text='Enter the title to display on the page, you can use only 255 characters.')),
                ('key_info', wagtail.core.fields.StreamField((('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())), help_text='Enter the body content for the KEY INFO summary tab. This content is for non-participating and new audiences')),
                ('in_depth', wagtail.core.fields.StreamField((('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())), help_text='Enter the body content for the IN-DEPTH summary tab. This content is for participants and experienced audiences')),
                ('call_to_action', models.ForeignKey(related_name='+', to='snippets.CallToAction', help_text='Specify the page you would like visitors to go to next.')),
                ('feed_image', models.ForeignKey(null=True, to='wagtailimages.Image', related_name='+', blank=True, on_delete=django.db.models.deletion.SET_NULL, help_text='This image will be used in listings and indexes across the site, if no feed image is added, the social image will be used.')),
                ('social_image', models.ForeignKey(null=True, to='wagtailimages.Image', related_name='+', blank=True, on_delete=django.db.models.deletion.SET_NULL, help_text="Image to appear alongside 'social text', particularly for sharing on social networks")),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page', models.Model),
        ),
        migrations.CreateModel(
            name='StandardPageRelatedLink',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('sort_order', models.IntegerField(null=True, blank=True, editable=False)),
                ('link_external', models.URLField(verbose_name='External link', blank=True)),
                ('title', models.CharField(max_length=255, help_text='Link title')),
                ('link_document', models.ForeignKey(null=True, related_name='+', blank=True, to='wagtaildocs.Document')),
                ('link_page', models.ForeignKey(null=True, related_name='+', blank=True, to='wagtailcore.Page')),
                ('page', modelcluster.fields.ParentalKey(to='standard.StandardPage', related_name='related_links')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
