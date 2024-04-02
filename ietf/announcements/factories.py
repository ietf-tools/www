import factory
import wagtail_factories

from ietf.utils.factories import StandardBlockFactory
from .models import IABAnnouncementIndexPage, IABAnnouncementPage


class IABAnnouncementPageFactory(wagtail_factories.PageFactory):
    title = factory.Faker("name")
    date = factory.Faker("date")
    introduction = factory.Faker("paragraph")
    body = wagtail_factories.StreamFieldFactory(StandardBlockFactory)

    class Meta:  # type: ignore
        model = IABAnnouncementPage


class IABAnnouncementIndexPageFactory(wagtail_factories.PageFactory):
    title = factory.Faker("name")
    introduction = factory.Faker("paragraph")

    class Meta:  # type: ignore
        model = IABAnnouncementIndexPage
