from wagtail.core.blocks import (
    CharBlock, RichTextBlock, StreamBlock, RawHTMLBlock
)
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtailmarkdown.blocks import MarkdownBlock


class StandardBlock(StreamBlock):
    heading = CharBlock(icon="title")
    paragraph = RichTextBlock(icon="pilcrow")
    image = ImageChooserBlock(icon="image", template='includes/imageblock.html')
    markdown = MarkdownBlock(icon="code")
    embed = EmbedBlock(icon="code")
    raw_html = RawHTMLBlock(icon="placeholder")
    table = TableBlock(table_options={'renderer': 'html'}, template="includes/tableblock.html")
