import factory
import wagtail_factories

from .models import EventListingPage, EventPage


class EventPageFactory(wagtail_factories.PageFactory):
    title = factory.Faker("name")
    introduction = factory.Faker("paragraph")

    class Meta:  # type: ignore
        model = EventPage


class EventListingPageFactory(wagtail_factories.PageFactory):
    title = factory.Faker("name")

    class Meta:  # type: ignore
        model = EventListingPage
