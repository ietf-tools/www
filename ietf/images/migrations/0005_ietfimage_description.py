# Generated by Django 4.2.17 on 2024-12-16 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0004_django_42_rendition_storage'),
    ]

    operations = [
        migrations.AddField(
            model_name='ietfimage',
            name='description',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='description'),
        ),
    ]
