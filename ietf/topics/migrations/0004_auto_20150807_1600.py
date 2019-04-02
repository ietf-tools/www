# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks
import modelcluster.fields
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0006_add_verbose_names'),
        ('topics', '0003_secondarytopicpageperson'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrimaryToSecondaryRelationship',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
            ],
        ),
        migrations.AddField(
            model_name='primarytopicpage',
            name='feed_image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtailimages.Image', related_name='+', null=True, help_text='This image will be used in listings and indexes across the site, if no feed image is added, the social image will be used.'),
        ),
        migrations.AddField(
            model_name='primarytopicpage',
            name='in_depth',
            field=wagtail.core.fields.StreamField((('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())), help_text='Enter the body content for the IN-DEPTH summary tab. This content is for participants and experienced audiences', default=[]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='primarytopicpage',
            name='introduction',
            field=models.CharField(max_length=255, help_text='Enter the title to display on the page, you can use only 255 characters.', default=[]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='primarytopicpage',
            name='key_info',
            field=wagtail.core.fields.StreamField((('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())), help_text='Enter the body content for the KEY INFO summary tab. This content is for non-participating and new audiences', default=[]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='primarytopicpage',
            name='social_image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtailimages.Image', related_name='+', null=True, help_text="Image to appear alongside 'social text', particularly for sharing on social networks"),
        ),
        migrations.AddField(
            model_name='primarytopicpage',
            name='social_text',
            field=models.CharField(max_length=255, blank=True, help_text='Description of this page as it should appear when shared on social networks, or in Google results'),
        ),
        migrations.AddField(
            model_name='primarytosecondaryrelationship',
            name='page',
            field=modelcluster.fields.ParentalKey(related_name='secondary_topics', to='topics.PrimaryTopicPage'),
        ),
        migrations.AddField(
            model_name='primarytosecondaryrelationship',
            name='secondary_topic',
            field=models.ForeignKey(related_name='+', to='topics.SecondaryTopicPage'),
        ),
    ]
