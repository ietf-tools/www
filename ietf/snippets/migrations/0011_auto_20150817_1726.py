# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0010_auto_20150814_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calltoaction',
            name='blurb',
            field=models.CharField(max_length=255, help_text='An explanation of the call to action.', blank=True),
        ),
        migrations.AlterField(
            model_name='calltoaction',
            name='button_text',
            field=models.CharField(max_length=255, help_text='Text that appears on the call to action link.'),
        ),
        migrations.AlterField(
            model_name='glossaryitem',
            name='body',
            field=models.TextField(help_text='Explanation of the glossary term.'),
        ),
        migrations.AlterField(
            model_name='glossaryitem',
            name='title',
            field=models.CharField(max_length=255, help_text='The glossary term.'),
        ),
        migrations.AlterField(
            model_name='mailinglistsignup',
            name='blurb',
            field=models.CharField(max_length=255, help_text='An explanation and call to action for this content.', blank=True),
        ),
        migrations.AlterField(
            model_name='mailinglistsignup',
            name='button_text',
            field=models.CharField(max_length=255, help_text='Text that appears on the mailing list link.'),
        ),
        migrations.AlterField(
            model_name='mailinglistsignup',
            name='sign_up',
            field=models.CharField(max_length=255, help_text='The URL or email address where the user should sign up. If the working group is set then this does not need to be set.', blank=True),
        ),
        migrations.AlterField(
            model_name='mailinglistsignup',
            name='title',
            field=models.CharField(max_length=255, help_text='The header text for this content.'),
        ),
        migrations.AlterField(
            model_name='mailinglistsignup',
            name='working_group',
            field=models.ForeignKey(related_name='+', null=True, on_delete=django.db.models.deletion.SET_NULL, help_text='The group whose mailing list sign up address should be used. If sign up is set then this does not need to be set.', to='datatracker.WorkingGroup', blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='bio',
            field=models.CharField(max_length=511, help_text="This person's professional background."),
        ),
        migrations.AlterField(
            model_name='person',
            name='email',
            field=models.EmailField(max_length=254, help_text="This person's email address."),
        ),
        migrations.AlterField(
            model_name='person',
            name='image',
            field=models.ForeignKey(related_name='+', help_text='A photograph of this person.', to='wagtailimages.Image'),
        ),
        migrations.AlterField(
            model_name='person',
            name='name',
            field=models.CharField(max_length=255, help_text="This person's full name."),
        ),
        migrations.AlterField(
            model_name='person',
            name='title',
            field=models.CharField(max_length=255, help_text="This person's role within the IETF."),
        ),
        migrations.AlterField(
            model_name='primarytopic',
            name='title',
            field=models.CharField(max_length=255, help_text='The name of this topic.'),
        ),
        migrations.AlterField(
            model_name='secondarytopic',
            name='title',
            field=models.CharField(max_length=255, help_text='The name of this topic.'),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='logo',
            field=models.ForeignKey(related_name='+', help_text="The organisation's logo.", to='wagtailimages.Image'),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='title',
            field=models.CharField(max_length=255, help_text='The name of the organisation.'),
        ),
    ]
