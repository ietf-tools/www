import factory
import wagtail_factories

from .models import FormPage


class FormPageFactory(wagtail_factories.PageFactory):
    title = factory.Faker("name")
    intro = factory.Faker("paragraph")
    thank_you_text = factory.Faker("paragraph")

    class Meta:  # type: ignore
        model = FormPage
