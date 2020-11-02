from django.test import TestCase

from .models import GlossaryPage
from ..home.models import HomePage

from wagtail.core.models import Page, Site

class FormPageTests(TestCase):

    def test_standard_page(self):

        root = Page.get_first_root_node()

        home = HomePage(
            slug = 'homepageslug',
            title = 'home page title',
            heading = 'home page heading',
            introduction = 'home page introduction',
            request_for_comments_section_body = 'rfc section body',
            working_groups_section_body = 'wg section body',
        )

        root.add_child(instance=home)

        Site.objects.all().delete()

        Site.objects.create(
            hostname='localhost',
            root_page = home,
            is_default_site=True,
            site_name='testingsitename',
        )

        glossary = GlossaryPage(
            slug = 'glossary',
            title = 'glossary title',
            introduction = 'glossary introduction',
        )
        home.add_child(instance = glossary)

        r = self.client.get(path=glossary.url or '/glossary')
        self.assertEqual(r.status_code, 200)

        self.assertIn(glossary.title.encode(), r.content)
        self.assertIn(glossary.introduction.encode(), r.content)
