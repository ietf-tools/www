import factory
import wagtail_factories

from .models import PrimaryTopicPage, TopicIndexPage


class PrimaryTopicPageFactory(wagtail_factories.PageFactory):
    title = factory.Faker("name")
    introduction = factory.Faker("paragraph")

    class Meta:  # type: ignore
        model = PrimaryTopicPage


class TopicIndexPageFactory(wagtail_factories.PageFactory):
    title = factory.Faker("name")
    introduction = factory.Faker("paragraph")

    class Meta:  # type: ignore
        model = TopicIndexPage
