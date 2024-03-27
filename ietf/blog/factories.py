import factory
import wagtail_factories

from .models import BlogIndexPage, BlogPage


class BlogPageFactory(wagtail_factories.PageFactory):
    title = factory.Faker("name")
    introduction = factory.Faker("paragraph")

    class Meta:  # type: ignore
        model = BlogPage


class BlogIndexPageFactory(wagtail_factories.PageFactory):
    title = factory.Faker("name")

    class Meta:  # type: ignore
        model = BlogIndexPage
