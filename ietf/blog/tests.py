from django.test import TestCase

from .models import BlogPage, BlogIndexPage
from ..home.models import HomePage

from wagtail.core.models import Page, Site

class BlogTests(TestCase):

    def test_blog(self):

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

        blogindex = BlogIndexPage(
            slug = 'blog',
            title = 'blog index title',
        )
        home.add_child(instance = blogindex)       

        nextblog = BlogPage(
            slug = 'nextpost',
            title = 'next title',
            introduction = 'next introduction',
            body = 'next body'
        )
        blogindex.add_child(instance = nextblog)

        otherblog = BlogPage(
            slug = 'otherpost',
            title = 'other title',
            introduction = 'other introduction',
            body = 'other body'
        )
        blogindex.add_child(instance = otherblog)

        prevblog = BlogPage(
            slug = 'prevpost',
            title = 'prev title',
            introduction = 'prev introduction',
            body = 'prev body'
        )
        blogindex.add_child(instance = prevblog)

        blog = BlogPage(
            slug = 'blogpost',
            title = 'blog title',
            introduction = 'blog introduction',
            body = 'blog body'
        )
        blogindex.add_child(instance = blog)

        r = self.client.get(path=blogindex.url or '/blog/all')
        self.assertEqual(r.status_code, 200)

        r = self.client.get(path=blog.url or '/blog')
        self.assertEqual(r.status_code, 200)

        self.assertIn(blog.title.encode(), r.content)
        self.assertIn(blog.introduction.encode(), r.content)
        # self.assertIn(blog.body.raw_text.encode(), r.content)
        self.assertIn(('href="%s"' % nextblog.url).encode(), r.content)
        self.assertIn(('href="%s"' % prevblog.url).encode(), r.content)
        self.assertIn(('href="%s"' % otherblog.url).encode(), r.content)
