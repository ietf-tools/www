import factory
import wagtail_factories
from factory.django import DjangoModelFactory

from .models import Person, Topic


class PersonFactory(DjangoModelFactory):
    name = factory.Faker("name")

    class Meta:  # type: ignore
        model = Person


class TopicFactory(DjangoModelFactory):
    title = factory.Faker("name")

    class Meta:  # type: ignore
        model = Topic
