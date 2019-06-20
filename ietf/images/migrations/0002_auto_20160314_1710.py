# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, connection


def copy_image_models(apps, schema_editor):
    cursor = connection.cursor()
    cursor.execute('INSERT INTO images_IETFImage (SELECT * from wagtailimages_image)')


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(copy_image_models),
    ]
