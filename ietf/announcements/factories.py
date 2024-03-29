import factory
import wagtail_factories

from .models import IABAnnouncementIndexPage, IABAnnouncementPage


class IABAnnouncementPageFactory(wagtail_factories.PageFactory):
    title = factory.Faker("name")
    introduction = factory.Faker("paragraph")

    class Meta:  # type: ignore
        model = IABAnnouncementPage


class IABAnnouncementIndexPageFactory(wagtail_factories.PageFactory):
    title = factory.Faker("name")
    introduction = factory.Faker("paragraph")

    class Meta:  # type: ignore
        model = IABAnnouncementIndexPage
