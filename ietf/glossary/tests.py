from django.test import TestCase
from wagtail.models import Page, Site

from ..home.models import HomePage
from .models import GlossaryPage


class GlossaryPageTests(TestCase):
    def test_glossary_page(self):

        root = Page.get_first_root_node()

        home = HomePage(
            slug="homepageslug",
            title="home page title",
            heading="home page heading",
            introduction="home page introduction",
        )

        root.add_child(instance=home)

        Site.objects.all().delete()

        Site.objects.create(
            hostname="localhost",
            root_page=home,
            is_default_site=True,
            site_name="testingsitename",
        )

        glossary = GlossaryPage(
            slug="glossary",
            title="glossary title",
            introduction="glossary introduction",
        )
        home.add_child(instance=glossary)

        r = self.client.get(path=glossary.url)
        self.assertEqual(r.status_code, 200)

        self.assertIn(glossary.title.encode(), r.content)
        self.assertIn(glossary.introduction.encode(), r.content)
