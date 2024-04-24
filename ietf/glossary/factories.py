import factory
import wagtail_factories

from .models import GlossaryPage


class GlossaryPageFactory(wagtail_factories.PageFactory):
    title = factory.Faker("name")
    introduction = factory.Faker("paragraph")

    class Meta:  # type: ignore
        model = GlossaryPage
