# Generated by Django 2.2.19 on 2021-11-01 01:13

import wagtail.blocks
import wagtail.contrib.table_block.blocks
import wagtail.embeds.blocks
import wagtail.fields
import wagtail.images.blocks
import wagtailmarkdown.blocks
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("standard", "0002_auto_20210325_0442"),
    ]

    operations = [
        migrations.AlterField(
            model_name="standardindexpage",
            name="in_depth",
            field=wagtail.fields.StreamField(
                [
                    ("heading", wagtail.blocks.CharBlock(icon="title")),
                    ("paragraph", wagtail.blocks.RichTextBlock(icon="pilcrow")),
                    (
                        "image",
                        wagtail.images.blocks.ImageChooserBlock(
                            icon="image", template="includes/imageblock.html"
                        ),
                    ),
                    ("markdown", wagtailmarkdown.blocks.MarkdownBlock(icon="code")),
                    ("embed", wagtail.embeds.blocks.EmbedBlock(icon="code")),
                    ("raw_html", wagtail.blocks.RawHTMLBlock(icon="placeholder")),
                    (
                        "table",
                        wagtail.contrib.table_block.blocks.TableBlock(
                            table_options={"renderer": "html"},
                            template="includes/tableblock.html",
                        ),
                    ),
                ],
                blank=True,
            ),
        ),
        migrations.AlterField(
            model_name="standardindexpage",
            name="key_info",
            field=wagtail.fields.StreamField(
                [
                    ("heading", wagtail.blocks.CharBlock(icon="title")),
                    ("paragraph", wagtail.blocks.RichTextBlock(icon="pilcrow")),
                    (
                        "image",
                        wagtail.images.blocks.ImageChooserBlock(
                            icon="image", template="includes/imageblock.html"
                        ),
                    ),
                    ("markdown", wagtailmarkdown.blocks.MarkdownBlock(icon="code")),
                    ("embed", wagtail.embeds.blocks.EmbedBlock(icon="code")),
                    ("raw_html", wagtail.blocks.RawHTMLBlock(icon="placeholder")),
                    (
                        "table",
                        wagtail.contrib.table_block.blocks.TableBlock(
                            table_options={"renderer": "html"},
                            template="includes/tableblock.html",
                        ),
                    ),
                ],
                blank=True,
            ),
        ),
        migrations.AlterField(
            model_name="standardpage",
            name="in_depth",
            field=wagtail.fields.StreamField(
                [
                    ("heading", wagtail.blocks.CharBlock(icon="title")),
                    ("paragraph", wagtail.blocks.RichTextBlock(icon="pilcrow")),
                    (
                        "image",
                        wagtail.images.blocks.ImageChooserBlock(
                            icon="image", template="includes/imageblock.html"
                        ),
                    ),
                    ("markdown", wagtailmarkdown.blocks.MarkdownBlock(icon="code")),
                    ("embed", wagtail.embeds.blocks.EmbedBlock(icon="code")),
                    ("raw_html", wagtail.blocks.RawHTMLBlock(icon="placeholder")),
                    (
                        "table",
                        wagtail.contrib.table_block.blocks.TableBlock(
                            table_options={"renderer": "html"},
                            template="includes/tableblock.html",
                        ),
                    ),
                ],
                blank=True,
            ),
        ),
        migrations.AlterField(
            model_name="standardpage",
            name="key_info",
            field=wagtail.fields.StreamField(
                [
                    ("heading", wagtail.blocks.CharBlock(icon="title")),
                    ("paragraph", wagtail.blocks.RichTextBlock(icon="pilcrow")),
                    (
                        "image",
                        wagtail.images.blocks.ImageChooserBlock(
                            icon="image", template="includes/imageblock.html"
                        ),
                    ),
                    ("markdown", wagtailmarkdown.blocks.MarkdownBlock(icon="code")),
                    ("embed", wagtail.embeds.blocks.EmbedBlock(icon="code")),
                    ("raw_html", wagtail.blocks.RawHTMLBlock(icon="placeholder")),
                    (
                        "table",
                        wagtail.contrib.table_block.blocks.TableBlock(
                            table_options={"renderer": "html"},
                            template="includes/tableblock.html",
                        ),
                    ),
                ],
                blank=True,
            ),
        ),
    ]
