from django.test import TestCase
from wagtail.models import Page, Site

from ..home.models import HomePage
from .models import StandardIndexPage, StandardPage


class StandardPageTests(TestCase):
    def test_standard_page(self):

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

        standardindex = StandardIndexPage(
            slug="standardindex",
            title="standard index page title",
            introduction="standard index page introduction",
        )
        home.add_child(instance=standardindex)

        standardpage = StandardPage(
            slug="standard",
            title="standard title",
            introduction="standard introduction",
        )
        standardindex.add_child(instance=standardpage)

        rindex = self.client.get(path=standardindex.url)
        self.assertEqual(rindex.status_code, 200)

        r = self.client.get(path=standardpage.url)
        self.assertEqual(r.status_code, 200)

        self.assertIn(standardpage.title.encode(), r.content)
        self.assertIn(standardpage.introduction.encode(), r.content)
        self.assertIn(('href="%s"' % standardindex.url).encode(), r.content)
