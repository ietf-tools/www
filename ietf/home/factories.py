import factory
import wagtail_factories

from .models import HomePage, IABHomePage


class HomePageFactory(wagtail_factories.PageFactory):
    title = factory.Faker("name")
    heading = factory.Faker("name")
    introduction = factory.Faker("name")

    class Meta:  # type: ignore
        model = HomePage


class IABHomePageFactory(wagtail_factories.PageFactory):
    title = factory.Faker("name")
    heading = factory.Faker("name")

    class Meta:  # type: ignore
        model = IABHomePage
