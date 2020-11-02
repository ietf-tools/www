from django.test import TestCase

from .models import FormPage
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

        form = FormPage(
            slug = 'form',
            title = 'form title',
            intro = 'form introduction',
        )
        home.add_child(instance = form)

        r = self.client.get(path=form.url or '/form')
        self.assertEqual(r.status_code, 200)

        self.assertIn(form.title.encode(), r.content)
        self.assertIn(form.intro.encode(), r.content)
