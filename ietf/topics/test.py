from django.test import TestCase
from wagtail.models import Page, Site

from ..home.models import HomePage
from .models import PrimaryTopicPage, TopicIndexPage


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

        topicindex = TopicIndexPage(
            slug="topicindex",
            title="topic index page title",
            introduction="topic index page introduction",
        )
        home.add_child(instance=topicindex)

        topicpage = PrimaryTopicPage(
            slug="topic",
            title="topic title",
            introduction="topic introduction",
        )
        topicindex.add_child(instance=topicpage)

        rindex = self.client.get(path=topicindex.url)
        self.assertEqual(rindex.status_code, 200)

        r = self.client.get(path=topicpage.url)
        self.assertEqual(r.status_code, 200)

        self.assertIn(topicpage.title.encode(), r.content)
        self.assertIn(topicpage.introduction.encode(), r.content)
        self.assertIn(('href="%s"' % topicindex.url).encode(), r.content)
