import factory
import wagtail_factories

from .models import IESGStatementIndexPage, IESGStatementPage


class IESGStatementPageFactory(wagtail_factories.PageFactory):
    title = factory.Faker("name")
    introduction = factory.Faker("paragraph")

    class Meta:  # type: ignore
        model = IESGStatementPage


class IESGStatementIndexPageFactory(wagtail_factories.PageFactory):
    title = factory.Faker("name")

    class Meta:  # type: ignore
        model = IESGStatementIndexPage
