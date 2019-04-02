# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.images.blocks
import wagtail.core.blocks
import django.db.models.deletion
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0006_add_verbose_names'),
        ('datatracker', '0002_area_active'),
        ('topics', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='secondarytopicpage',
            name='area',
            field=models.ForeignKey(to='datatracker.Area', related_name='+', default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='secondarytopicpage',
            name='feed_image',
            field=models.ForeignKey(help_text='This image will be used in listings and indexes across the site, if no feed image is added, the social image will be used.', on_delete=django.db.models.deletion.SET_NULL, related_name='+', blank=True, null=True, to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='secondarytopicpage',
            name='in_depth',
            field=wagtail.core.fields.StreamField((('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())), help_text='Enter the body content for the IN-DEPTH summary tab. This content is for participants and experienced audiences', default=[]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='secondarytopicpage',
            name='introduction',
            field=models.CharField(help_text='Enter the title to display on the page, you can use only 255 characters.', default=[], max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='secondarytopicpage',
            name='key_info',
            field=wagtail.core.fields.StreamField((('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())), help_text='Enter the body content for the KEY INFO summary tab. This content is for non-participating and new audiences', default=[]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='secondarytopicpage',
            name='social_image',
            field=models.ForeignKey(help_text="Image to appear alongside 'social text', particularly for sharing on social networks", on_delete=django.db.models.deletion.SET_NULL, related_name='+', blank=True, null=True, to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='secondarytopicpage',
            name='social_text',
            field=models.CharField(help_text='Description of this page as it should appear when shared on social networks, or in Google results', max_length=255, blank=True),
        ),
    ]
