import factory
from django.utils.text import slugify
from factory.django import DjangoModelFactory

from .models import Charter, MailingListSignup, Person, Topic, WorkingGroup


class PersonFactory(DjangoModelFactory):
    name = factory.Faker("name")
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))
    link = factory.Faker("url")

    class Meta:  # type: ignore
        model = Person


class TopicFactory(DjangoModelFactory):
    title = factory.Faker("name")
    slug = factory.LazyAttribute(lambda obj: slugify(obj.title))

    class Meta:  # type: ignore
        model = Topic


class CharterFactory(DjangoModelFactory):
    name = factory.Faker("name")

    class Meta:  # type: ignore
        model = Charter


class WorkingGroupFactory(DjangoModelFactory):
    name = factory.Faker("name")
    list_subscribe = factory.Faker("url")

    class Meta:  # type: ignore
        model = WorkingGroup


class MailingListSignupFactory(DjangoModelFactory):
    title = factory.Faker("name")
    blurb = factory.Faker("paragraph")
    button_text = factory.Faker("name")
    sign_up = factory.Faker("url")

    class Meta:  # type: ignore
        model = MailingListSignup
