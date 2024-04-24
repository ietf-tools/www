import factory
import wagtail_factories

from . import blocks


class StandardBlockFactory(wagtail_factories.StreamBlockFactory):
    heading = factory.SubFactory(wagtail_factories.CharBlockFactory)

    class Meta:
        model = blocks.StandardBlock
