from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
)
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.core.models import Orderable
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtailorderable.models import Orderable as WagtailOrderable


class LinkFields(models.Model):
    link_external = models.URLField("External link", blank=True)
    link_page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.CASCADE,
    )
    link_document = models.ForeignKey(
        "wagtaildocs.Document",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.CASCADE,
    )

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_document:
            return self.link_document.url
        else:
            return self.link_external

    panels = [
        FieldPanel("link_external"),
        PageChooserPanel("link_page"),
        DocumentChooserPanel("link_document"),
    ]

    class Meta:
        abstract = True


class RelatedLink(LinkFields):
    title = models.CharField(max_length=255, help_text="Link title")

    panels = [
        FieldPanel("title"),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    class Meta:
        abstract = True


class PromoteMixin(models.Model):
    social_text = models.CharField(
        max_length=255,
        blank=True,
        help_text="Description of this page as it should appear when shared on social networks, or in Google results",
    )
    social_image = models.ForeignKey(
        "images.IETFImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Image to appear alongside 'social text', particularly for sharing on social networks",
    )
    feed_image = models.ForeignKey(
        "images.IETFImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="This image will be used in listings and indexes across the site, if no feed image is added, the social image will be used.",
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("social_text"),
                ImageChooserPanel("social_image"),
                ImageChooserPanel("feed_image"),
            ],
            "Social/Meta descriptions",
        )
    ]

    class Meta:
        abstract = True


class SubMenuItem(Orderable):
    parent = ParentalKey("utils.MenuItem", related_name="sub_menu_items")
    page = models.ForeignKey(
        "wagtailcore.Page",
        related_name="+",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    link = models.URLField(blank=True)
    text = models.CharField(max_length=40, blank=True)

    @property
    def url(self):
        return self.link or getattr(self.page, "url", "")

    @property
    def title(self):
        return self.text or getattr(self.page, "title", "")

    panels = [PageChooserPanel("page"), FieldPanel("link"), FieldPanel("text")]


class MenuItem(ClusterableModel, WagtailOrderable):
    page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    text = models.CharField(max_length=40, blank=True)
    panels = [
        FieldPanel("text"),
        PageChooserPanel("page"),
        InlinePanel(
            "sub_menu_items",
            label="Sub Menu Items",
        ),
    ]

    @property
    def is_dropdown(self):
        return bool(self.sub_menu_items.count())

    @property
    def title(self):
        return self.text or getattr(self.page, "title", "")


@register_setting
class SocialMediaSettings(BaseSetting):
    twitter_handle = models.CharField(
        max_length=255,
        help_text="Your Twitter username without the @, e.g. flickr",
        blank="True",
    )
    facebook_app_id = models.CharField(
        max_length=255,
        help_text="Your Facebook app id",
        blank="True",
    )
    default_sharing_text = models.CharField(
        max_length=255,
        blank="True",
        help_text="Default sharing text to use if social text has not been set on a page.",
    )
    default_sharing_image = models.ForeignKey(
        "images.IETFImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Default sharing image to use if social image has not been set on a page.",
    )
    site_name = models.CharField(
        max_length=255,
        default=settings.WAGTAIL_SITE_NAME,
        blank="True",
        help_text="Site name, used by facebook open graph.",
    )

    panels = [
        FieldPanel("twitter_handle"),
        FieldPanel("facebook_app_id"),
        FieldPanel("default_sharing_text"),
        ImageChooserPanel("default_sharing_image"),
        FieldPanel("site_name"),
    ]


class FooterLinkItem(Orderable, LinkFields):
    title = models.CharField(max_length=255)
    model = ParentalKey("utils.FooterLinks", related_name="footer_link_items")

    panels = [
        FieldPanel("title"),
    ] + LinkFields.panels


@register_setting
class FooterLinks(BaseSetting, ClusterableModel):
    panels = [
        InlinePanel("footer_link_items", label="Footer Links"),
    ]


@register_setting
class FeedSettings(BaseSetting):
    blog_feed_title = models.CharField(
        max_length=255,
        blank=True,
    )
    blog_feed_description = models.CharField(
        max_length=255,
        blank=True,
    )

    class Meta:
        verbose_name = "Feeds"
