from wagtail.blocks import (
    CharBlock,
    FloatBlock,
    RawHTMLBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
)
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.contrib.typed_table_block.blocks import TypedTableBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtailmarkdown.blocks import MarkdownBlock

from django.conf import settings


class NoteWellBlock(StructBlock):
    def get_context(self, value):
        context = super().get_context(value)
        context['note_well_git_url'] = settings.NOTE_WELL_REPO
        return context

    class Meta:
        template = "blocks/note_well_block.html"


class StandardBlock(StreamBlock):
    heading = CharBlock(icon="title")
    paragraph = RichTextBlock(icon="pilcrow")
    image = ImageChooserBlock(icon="image", template="includes/imageblock.html")
    markdown = MarkdownBlock(icon="code")
    embed = EmbedBlock(icon="code")
    raw_html = RawHTMLBlock(icon="placeholder")
    table = TableBlock(
        table_options={"renderer": "html"}, template="includes/tableblock.html"
    )
    typed_table = TypedTableBlock(
        [
            ("text", CharBlock()),
            ("numeric", FloatBlock()),
            ("rich_text", RichTextBlock()),
            ("image", ImageChooserBlock()),
        ]
    )
    note_well = NoteWellBlock(icon="placeholder", label="Note Well Text")