from django.utils.functional import cached_property
from wagtail.blocks import (
    CharBlock,
    FloatBlock,
    ListBlock,
    PageChooserBlock,
    RawHTMLBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
    StructValue,
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


class LinkStructValue(StructValue):
    @cached_property
    def url(self):
        if external_url := self.get("external_url"):
            return external_url

        if page := self.get("page"):
            return page.url

        return ""

    @cached_property
    def text(self):
        if title := self.get("title"):
            return title

        if page := self.get("page"):
            return page.title

        return self.get("external_url")


class LinkBlock(StructBlock):
    page = PageChooserBlock(label="Page", required=False)
    title = CharBlock(label="Link text", required=False)
    external_url = URLBlock(label="External URL", required=False)

    class Meta:  # type: ignore
        value_class = LinkStructValue


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
            ("text", CharBlock()),
            ("numeric", FloatBlock()),
            ("rich_text", RichTextBlock()),
            ("image", ImageChooserBlock()),
        ]
    )
    note_well = NoteWellBlock(icon="placeholder", label="Note Well Text")
