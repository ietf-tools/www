from django.test import TestCase
from django.urls import reverse
from wagtail.models import Page, Site

from ..blog.models import BlogIndexPage, BlogPage
from ..home.models import HomePage


class SearchTests(TestCase):
    def test_search(self):

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

        blogindex = BlogIndexPage(
            slug="blog",
            title="blog index title",
        )
        home.add_child(instance=blogindex)

        blog = BlogPage(
            slug="blogpost",
            title="blog title",
            introduction="blog introduction",
            body='[{"id": "1", "type": "rich_text", "value": "<p>blog body</p>"}]',
        )
        blogindex.add_child(instance=blog)

        home.button_text = "blog button text"
        home.button_link = blog
        home.save()

        resp = self.client.get(f"{reverse('search')}?query=introduction")

        self.assertEqual(resp.context["search_query"], "introduction")
        self.assertEqual(
            list(resp.context["search_results"]),
            [Page.objects.get(pk=blog.pk)],
        )
