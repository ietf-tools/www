# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0017_remove_secondarytopicpageperson_person'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='secondarytopicpageperson',
            name='page',
        ),
        migrations.DeleteModel(
            name='SecondaryTopicPagePerson',
        ),
    ]
