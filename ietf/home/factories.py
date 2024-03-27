import factory
import wagtail_factories

from .models import HomePage


class HomePageFactory(wagtail_factories.PageFactory):
    title = factory.Faker("name")
    heading = factory.Faker("name")
    introduction = factory.Faker("name")

    class Meta:  # type: ignore
        model = HomePage
