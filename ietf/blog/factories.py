import factory
import wagtail_factories

from ietf.utils.factories import StandardBlockFactory

from .models import BlogIndexPage, BlogPage


class BlogPageFactory(wagtail_factories.PageFactory):
    title = factory.Faker("name")
    introduction = factory.Faker("paragraph")
    body = wagtail_factories.StreamFieldFactory(StandardBlockFactory)

    class Meta:  # type: ignore
        model = BlogPage


class BlogIndexPageFactory(wagtail_factories.PageFactory):
    title = factory.Faker("name")

    class Meta:  # type: ignore
        model = BlogIndexPage
