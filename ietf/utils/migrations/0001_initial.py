# Generated by Django 1.11.29 on 2020-04-10 18:46

import django.db.models.deletion
import modelcluster.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("images", "0001_initial"),
        ("wagtaildocs", "0008_document_file_size"),
        ("wagtailcore", "0040_page_draft_title"),
    ]

    operations = [
        migrations.CreateModel(
            name="FeedSettings",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("blog_feed_title", models.CharField(blank=True, max_length=255)),
                ("blog_feed_description", models.CharField(blank=True, max_length=255)),
                (
                    "site",
                    models.OneToOneField(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="wagtailcore.Site",
                    ),
                ),
            ],
            options={
                "verbose_name": "Feeds",
            },
        ),
        migrations.CreateModel(
            name="FooterLinkItem",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "sort_order",
                    models.IntegerField(blank=True, editable=False, null=True),
                ),
                (
                    "link_external",
                    models.URLField(blank=True, verbose_name="External link"),
                ),
                ("title", models.CharField(max_length=255)),
                (
                    "link_document",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="wagtaildocs.Document",
                    ),
                ),
                (
                    "link_page",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="wagtailcore.Page",
                    ),
                ),
            ],
            options={
                "ordering": ["sort_order"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="FooterLinks",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "site",
                    models.OneToOneField(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="wagtailcore.Site",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="SecondaryMenu",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "contact_page",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailcore.Page",
                    ),
                ),
                (
                    "site",
                    models.OneToOneField(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="wagtailcore.Site",
                    ),
                ),
                (
                    "tools_page",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailcore.Page",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="SocialMediaSettings",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "twitter_handle",
                    models.CharField(
                        blank="True",
                        help_text="Your Twitter username without the @, e.g. flickr",
                        max_length=255,
                    ),
                ),
                (
                    "facebook_app_id",
                    models.CharField(
                        blank="True", help_text="Your Facebook app id", max_length=255
                    ),
                ),
                (
                    "default_sharing_text",
                    models.CharField(
                        blank="True",
                        help_text="Default sharing text to use if social text has not been set on a page.",
                        max_length=255,
                    ),
                ),
                (
                    "site_name",
                    models.CharField(
                        blank="True",
                        default="ietf",
                        help_text="Site name, used by facebook open graph.",
                        max_length=255,
                    ),
                ),
                (
                    "default_sharing_image",
                    models.ForeignKey(
                        blank=True,
                        help_text="Default sharing image to use if social image has not been set on a page.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="images.IETFImage",
                    ),
                ),
                (
                    "site",
                    models.OneToOneField(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="wagtailcore.Site",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ToolsMenuItem",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "sort_order",
                    models.IntegerField(blank=True, editable=False, null=True),
                ),
                ("link", models.URLField(blank=True)),
                ("text", models.CharField(blank=True, max_length=255)),
                (
                    "model",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tools_menu_items",
                        to="utils.SecondaryMenu",
                    ),
                ),
                (
                    "page",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailcore.Page",
                    ),
                ),
            ],
            options={
                "ordering": ["sort_order"],
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="footerlinkitem",
            name="model",
            field=modelcluster.fields.ParentalKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="footer_link_items",
                to="utils.FooterLinks",
            ),
        ),
    ]
