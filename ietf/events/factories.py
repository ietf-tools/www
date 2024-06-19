import factory
import wagtail_factories

from ietf.utils.factories import StandardBlockFactory

from .models import EventListingPage, EventPage


class EventPageFactory(wagtail_factories.PageFactory):
    title = factory.Faker("name")
    introduction = factory.Faker("paragraph")
    body = wagtail_factories.StreamFieldFactory(StandardBlockFactory)

    class Meta:  # type: ignore
        model = EventPage


class EventListingPageFactory(wagtail_factories.PageFactory):
    title = factory.Faker("name")

    class Meta:  # type: ignore
        model = EventListingPage
