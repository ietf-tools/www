# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

def forward(apps, schema_editor):

    Charter = apps.get_model('snippets','Charter')
    WorkingGroup = apps.get_model('snippets','WorkingGroup')

    for charter in Charter.objects.all():
        acronym = charter.name.split('-')[-1]
        charter.working_group = WorkingGroup.objects.get(acronym=acronym)
        charter.save()

def reverse(apps, schema_editor):
    """ There's no sense in reversing this """
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0044_add_snippets'),
    ]

    operations = [
        migrations.RunPython(forward,reverse)
    ]