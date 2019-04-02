# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0001_initial'),
        ('snippets', '0023_group_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='image',
            field=models.ForeignKey(related_name='+', blank=True, to='images.IETFImage', help_text='An image to represent this group.', null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='image',
            field=models.ForeignKey(related_name='+', blank=True, to='images.IETFImage', help_text='A photograph of this person.', null=True),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='logo',
            field=models.ForeignKey(related_name='+', to='images.IETFImage', help_text="The organisation's logo."),
        ),
    ]
