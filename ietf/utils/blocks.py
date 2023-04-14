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

from ietf.utils.models import TextChunk


class NoteWellBlock(StructBlock):
    def get_context(self, value, parent_context=None):
        context = super(NoteWellBlock, self).get_context(value, parent_context)
        note_well, created = TextChunk.objects.get_or_create(slug="note-well")
        context.update(note_well=note_well)
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
    note_well = NoteWellBlock()
