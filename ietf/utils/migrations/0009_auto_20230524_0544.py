# Generated by Django 3.2.13 on 2023-05-24 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0008_auto_20230524_0536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socialmediasettings',
            name='linkedin',
            field=models.CharField(blank='True', help_text='Link to linkedin profile', max_length=255, verbose_name='LinkedIn link'),
        ),
        migrations.AlterField(
            model_name='socialmediasettings',
            name='mastodon',
            field=models.CharField(blank='True', help_text='Link to mastodon profile', max_length=255, verbose_name='Mastodon link'),
        ),
        migrations.AlterField(
            model_name='socialmediasettings',
            name='twitter',
            field=models.CharField(blank='True', help_text='Link to twitter profile', max_length=255, verbose_name='Twitter link'),
        ),
        migrations.AlterField(
            model_name='socialmediasettings',
            name='youtube',
            field=models.CharField(blank='True', help_text='Link to youtube account', max_length=255, verbose_name='Youtube link'),
        ),
    ]
