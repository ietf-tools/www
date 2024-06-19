# Generated by Django 2.2.19 on 2021-03-25 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("forms", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="formfield",
            name="clean_name",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Safe name of the form field, the label converted to ascii_snake_case",
                max_length=255,
                verbose_name="name",
            ),
        ),
    ]
