from django.conf import settings
from django.db import models
from django.template.loader import get_template
from wagtail.admin.panels import FieldPanel, TitleFieldPanel
from wagtail.admin.widgets.slug import SlugInput
from wagtail.fields import RichTextField
from wagtail.search import index
from wagtail.search.index import Indexed
from wagtail.snippets.models import register_snippet

from ..utils.models import RelatedLink


class RenderableSnippetMixin:
    def render(self):
        template = get_template(self.TEMPLATE_NAME)
        return template.render({"snippet": self})


@register_snippet
class Charter(models.Model, index.Indexed):
    name = models.CharField(max_length=511, unique=True)
    title = models.TextField(blank=True)
    abstract = models.TextField(blank=True)
    working_group = models.ForeignKey(
        "snippets.WorkingGroup",
        blank=True,
        null=True,
        related_name="+",
        help_text="This charter's working group",
        on_delete=models.CASCADE,
    )

    search_fields = [
        index.SearchField("title", boost=10),
        index.AutocompleteField("title", boost=10),
        index.SearchField("abstract"),
        index.AutocompleteField("abstract"),
    ]

    def __str__(self):  # pragma: no cover
        return self.title

    @property
    def url(self):
        if self.working_group:
            return self.working_group.charter_url
        else:
            return ""

    class Meta:
        ordering = ["title"]
        verbose_name = "Charter"


@register_snippet
class WorkingGroup(models.Model, index.Indexed):

    name = models.CharField(max_length=511)
    acronym = models.CharField(max_length=511, blank=True)
    description = models.CharField(max_length=4096, blank=True)
    list_email = models.EmailField(blank=True)
    list_subscribe = models.URLField(blank=True)
    # There is no field currently to capture area/parent

    search_fields = [
        index.SearchField("name", boost=10),
        index.AutocompleteField("name", boost=10),
        index.SearchField("acronym"),
        index.AutocompleteField("acronym"),
        index.SearchField("description"),
        index.AutocompleteField("description"),
    ]

    @property
    def url(self):
        return settings.DATATRACKER_URI + "/group/" + self.acronym

    @property
    def charter_url(self):
        return self.url + "/charter/"

    def __str__(self):  # pragma: no cover
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Working Group"


@register_snippet
class RFC(models.Model, index.Indexed):

    name = models.CharField(max_length=511)
    title = models.TextField(blank=True)
    rfc = models.CharField(
        max_length=511, unique=True, help_text="The RFC's number (without any letters)"
    )
    abstract = models.TextField(blank=True)
    # There is currently no field for authors
    working_group = models.ForeignKey(
        "snippets.WorkingGroup",
        blank=True,
        null=True,
        related_name="+",
        help_text="The working group that produced this RFC",
        on_delete=models.SET_NULL,
    )

    search_fields = [
        index.SearchField("title", boost=10),
        index.AutocompleteField("title", boost=10),
        index.SearchField("rfc", boost=10),
        index.AutocompleteField("rfc", boost=10),
        index.SearchField("authors"),
        index.AutocompleteField("authors"),
        index.SearchField("abstract"),
        index.AutocompleteField("abstract"),
    ]

    def __str__(self):  # pragma: no cover
        return f"RFC {self.rfc}"

    @property
    def long_title(self):
        return self.title

    @property
    def url(self):
        return settings.DATATRACKER_URI + "/doc/rfc" + self.rfc

    class Meta:
        ordering = ["title"]
        verbose_name = "RFC"


@register_snippet
class Person(models.Model, Indexed):
    name = models.CharField(max_length=511)
    slug = models.SlugField(max_length=511, unique=True)
    link = models.URLField()

    search_fields = [
        index.SearchField("name"),
        index.AutocompleteField("name"),
    ]
    panels = [
        TitleFieldPanel("name"),
        FieldPanel("slug", widget=SlugInput),
    ]

    def __str__(self):  # pragma: no cover
        return self.name

    class Meta:
        ordering = ["name"]


@register_snippet
class Role(models.Model, Indexed):
    name = models.CharField(max_length=255, help_text="A role within the IETF.")

    search_fields = [
        index.SearchField("name"),
        index.AutocompleteField("name"),
    ]

    panels = [FieldPanel("name")]

    def __str__(self):  # pragma: no cover
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Role Override"


@register_snippet
class Group(models.Model, Indexed, RenderableSnippetMixin):
    """
    A group of people within the IETF. Groups may appear on the site as
    :model:`blog.BlogPage` author groups.
    """

    name = models.CharField(max_length=255, help_text="This group's name.")
    role = models.ForeignKey(
        "snippets.Role",
        blank=True,
        null=True,
        related_name="+",
        help_text="This group's role within the IETF.",
        on_delete=models.SET_NULL,
    )
    summary = models.CharField(
        blank=True, max_length=511, help_text="More information about this group."
    )
    email = models.EmailField(blank=True, help_text="This group's email address.")
    image = models.ForeignKey(
        "images.IETFImage",
        blank=True,
        null=True,
        related_name="+",
        help_text="An image to represent this group.",
        on_delete=models.SET_NULL,
    )

    search_fields = [
        index.SearchField("name"),
        index.AutocompleteField("name"),
        index.SearchField("summary"),
        index.AutocompleteField("summary"),
        index.SearchField("email"),
        index.AutocompleteField("email"),
    ]

    panels = [
        FieldPanel("name"),
        FieldPanel("role"),
        FieldPanel("summary"),
        FieldPanel("email"),
        FieldPanel("image"),
    ]

    def __str__(self):  # pragma: no cover
        return self.name

    TEMPLATE_NAME = "snippets/group.html"

    class Meta:
        ordering = ["name"]


@register_snippet
class CallToAction(Indexed, RelatedLink, RenderableSnippetMixin):
    """
    Content that guides the user to the next step after having
    read a page.
    """

    blurb = models.CharField(
        max_length=255, blank=True, help_text="An explanation of the call to action."
    )
    button_text = models.CharField(
        max_length=255, help_text="Text that appears on the call to action link."
    )

    search_fields = [
        index.SearchField("title"),
        index.AutocompleteField("title"),
        index.SearchField("blurb"),
        index.AutocompleteField("blurb"),
        index.SearchField("button_text"),
        index.AutocompleteField("button_text"),
    ]

    panels = RelatedLink.panels + [
        FieldPanel("blurb"),
        FieldPanel("button_text"),
    ]

    def __str__(self):  # pragma: no cover
        return self.title

    TEMPLATE_NAME = "snippets/call_to_action.html"

    class Meta:
        verbose_name_plural = "Calls to action"
        ordering = ["title"]


@register_snippet
class MailingListSignup(models.Model, Indexed, RenderableSnippetMixin):
    """
    Page content that directs users to a mailing list sign up link
    or address.
    """

    title = models.CharField(
        max_length=255, help_text="The header text for this content."
    )
    blurb = models.CharField(
        max_length=255,
        blank=True,
        help_text="An explanation and call to action for this content.",
    )
    button_text = models.CharField(
        max_length=255, help_text="Text that appears on the mailing list link."
    )
    sign_up = models.CharField(
        max_length=255,
        blank=True,
        help_text="The URL or email address where the user should sign up. "
        "If the working group is set then this does not need to be set.",
    )
    working_group = models.ForeignKey(
        "snippets.WorkingGroup",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="The group whose mailing list sign up address should be "
        "used. If sign up is set then this does not need to be set.",
    )

    search_fields = [
        index.SearchField("title"),
        index.AutocompleteField("title"),
        index.SearchField("blurb"),
        index.AutocompleteField("blurb"),
        index.SearchField("button_text"),
        index.AutocompleteField("button_text"),
        index.SearchField("sign_up"),
        index.AutocompleteField("sign_up"),
    ]

    panels = [
        FieldPanel("title"),
        FieldPanel("blurb"),
        FieldPanel("button_text"),
        FieldPanel("sign_up"),
        FieldPanel("working_group"),
    ]

    @property
    def link(self):
        if self.sign_up:
            link = self.sign_up
        else:
            link = self.working_group.list_subscribe

        if "@" in link:
            return f"mailto:{link}"
        else:
            return link

    TEMPLATE_NAME = "snippets/mailing_list_signup.html"

    def __str__(self):  # pragma: no cover
        return self.title

    class Meta:
        ordering = ["title"]


@register_snippet
class Topic(models.Model, Indexed):
    """
    These snippets categorise blog posts.
    """

    title = models.CharField(max_length=255, help_text="The name of this topic.")
    slug = models.CharField(max_length=511, unique=True)

    search_fields = [
        index.SearchField("title"),
        index.AutocompleteField("title"),
        index.SearchField("slug"),
        index.AutocompleteField("slug"),
    ]

    panels = [
        TitleFieldPanel("title"),
        FieldPanel("slug", widget=SlugInput),
    ]

    def __str__(self):  # pragma: no cover
        return self.title

    class Meta:
        ordering = ["title"]


@register_snippet
class Sponsor(models.Model, Indexed):
    """
    An organisation that sponsors IETF events.
    """

    title = models.CharField(max_length=255, help_text="The name of the organisation.")
    logo = models.ForeignKey(
        "images.IETFImage",
        related_name="+",
        help_text="The organisation's logo.",
        on_delete=models.CASCADE,
    )
    link = models.URLField(blank=True)

    search_fields = [
        index.SearchField("title"),
        index.AutocompleteField("title"),
    ]

    panels = [FieldPanel("title"), FieldPanel("logo"), FieldPanel("link")]

    def __str__(self):  # pragma: no cover
        return self.title

    class Meta:
        ordering = ["title"]


@register_snippet
class GlossaryItem(models.Model, Indexed):
    """
    A short explanation of a technical term.
    Appears on the :models:`glossary.GlossaryPage`.
    """

    title = models.CharField(max_length=255, help_text="The glossary term.")
    body = RichTextField(help_text="Explanation of the glossary term.")
    link = models.URLField(blank=True)

    search_fields = [
        index.SearchField("title"),
        index.AutocompleteField("title"),
        index.SearchField("body"),
        index.AutocompleteField("body"),
    ]

    panels = [
        FieldPanel("title"),
        FieldPanel("body"),
        FieldPanel("link"),
    ]

    def __str__(self):  # pragma: no cover
        return self.title

    @property
    def url(self):
        from ietf.glossary.models import GlossaryPage

        return f"{GlossaryPage.objects.first().url}?query={self.title}"

    class Meta:
        ordering = ["title"]
        verbose_name = "Glossary item"
