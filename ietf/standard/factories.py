import factory
import wagtail_factories

from .models import StandardIndexPage, StandardPage


class StandardPageFactory(wagtail_factories.PageFactory):
    title = factory.Faker("name")
    introduction = factory.Faker("paragraph")

    class Meta:  # type: ignore
        model = StandardPage


class StandardIndexPageFactory(wagtail_factories.PageFactory):
    title = factory.Faker("name")

    class Meta:  # type: ignore
        model = StandardIndexPage
