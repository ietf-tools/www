import factory
from factory.django import DjangoModelFactory

from .models import Person


class PersonFactory(DjangoModelFactory):
    name = factory.Faker("name")

    class Meta:  # type: ignore
        model = Person
