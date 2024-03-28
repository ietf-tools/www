from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import StreamField
from wagtail.models import Orderable, PreviewableMixin, Site
from wagtailorderable.models import Orderable as WagtailOrderable

from ietf.utils.blocks import MainMenuSection


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
        FieldPanel("link_page"),
        FieldPanel("link_document"),
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
                FieldPanel("social_image"),
                FieldPanel("feed_image"),
            ],
            "Social/Meta descriptions",
        )
    ]

    class Meta:
        abstract = True

    def get_social_image(self):
        return self.social_image

    def get_social_text(self):
        return self.social_text or self.search_description


class MainMenuItem(PreviewableMixin, models.Model):
    page = models.ForeignKey("wagtailcore.Page", related_name="+", on_delete=models.CASCADE)
    image = models.ForeignKey(
        "images.IETFImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        # help_text="Image to appear alongside 'social text', particularly for sharing on social networks",
    )
    secondary_sections = StreamField(
        [
            ("section", MainMenuSection()),
        ],
        blank=True,
        use_json_field=True,
    )
    sort_order = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ["sort_order"]

    def __str__(self):  # pragma: no cover
        return self.page.title

    def get_preview_template(self, request, mode_name):
        return "previews/main_menu_item.html"

    def get_preview_context(self, request, mode_name):
        from .context_processors import PreviewMainMenu

        site = Site.find_for_request(request)

        return {
            **super().get_preview_context(request, mode_name),
            "MENU": PreviewMainMenu(site, self).get_menu(),
            "MENU_PREVIEW": self,
        }


class SubMenuItem(Orderable):
    parent = ParentalKey("utils.SecondaryMenuItem", related_name="sub_menu_items")
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

    panels = [FieldPanel("page"), FieldPanel("link"), FieldPanel("text")]


class SecondaryMenuItem(ClusterableModel, WagtailOrderable):
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
        FieldPanel("page"),
        InlinePanel(
            "sub_menu_items",
            label="Sub Menu Items",
        ),
    ]

    @property
    def is_dropdown(self):
        return self.sub_menu_items.exists()

    @property
    def title(self):
        return self.text or getattr(self.page, "title", "")

    class Meta:
        verbose_name_plural = "Secondary Menu"


@register_setting
class SocialMediaSettings(BaseSiteSetting):
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

    linkedin = models.CharField(
        max_length=255,
        help_text="Link to LinkedIn profile",
        blank="True",
        verbose_name="LinkedIn link"
    )
    twitter = models.CharField(
        max_length=255,
        help_text="Link to Twitter profile",
        blank="True",
        verbose_name="Twitter link"
    )
    youtube = models.CharField(
        max_length=255,
        help_text="Link to YouTube account",
        blank="True",
        verbose_name="Youtube link"
    )
    mastodon = models.CharField(
        max_length=255,
        help_text="Link to Mastodon profile",
        blank="True",
        verbose_name="Mastodon link"
    )
    github = models.CharField(
        max_length=255,
        help_text="Link to GitHub profile",
        blank="True",
        verbose_name="GitHub link"
    )
    
    panels = [
        FieldPanel("twitter_handle"),
        FieldPanel("facebook_app_id"),
        FieldPanel("default_sharing_text"),
        FieldPanel("default_sharing_image"),
        FieldPanel("site_name"),
        FieldPanel("linkedin"),
        FieldPanel("twitter"),
        FieldPanel("youtube"),
        FieldPanel("mastodon"),
        FieldPanel("github"),
    ]


class FooterLinkItem(Orderable, LinkFields):
    title = models.CharField(max_length=255)
    model = ParentalKey("utils.FooterLinks", related_name="footer_link_items")

    panels = [
        FieldPanel("title"),
    ] + LinkFields.panels


@register_setting
class FooterLinks(BaseSiteSetting, ClusterableModel):
    panels = [
        InlinePanel("footer_link_items", label="Footer Links"),
    ]


@register_setting
class FeedSettings(BaseSiteSetting):
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


DEFAULT_BASE = "base.html"
IAB_BASE = "iab_base.html"
BASE_TEMPLATE_CHOICES = (
    (DEFAULT_BASE, "IETF (default)"),
    (IAB_BASE, "IAB"),
)


@register_setting
class LayoutSettings(BaseSiteSetting):
    base_template = models.CharField(
        max_length=255,
        blank=True,
        choices=BASE_TEMPLATE_CHOICES,
        default="base.html",
    )


class TextChunk(models.Model):
    slug = models.SlugField(blank=False, null=False)
    text = models.TextField()
