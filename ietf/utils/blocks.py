from wagtail.blocks import (
    CharBlock,
    FloatBlock,
    ListBlock,
    PageChooserBlock,
    RawHTMLBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
    URLBlock,
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


class LinkBlock(StructBlock):
    page = PageChooserBlock(label="Page", required=False)
    title = CharBlock(label="Link text", required=False)
    external_url = URLBlock(label="External URL", required=False)


class MainMenuSection(StructBlock):
    title = CharBlock(label="Section title", required=True)
    links = ListBlock(LinkBlock())


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
            ("text", CharBlock(required=False)),
            ("numeric", FloatBlock(required=False, template="blocks/float_block.html")),
            ("rich_text", RichTextBlock(required=False)),
            ("image", ImageChooserBlock(required=False)),
        ]
    )
    note_well = NoteWellBlock(icon="placeholder", label="Note Well Text")
