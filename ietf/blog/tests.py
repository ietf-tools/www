from django.test import TestCase
from datetime import datetime, timedelta

from .models import BlogPage, BlogIndexPage
from ..home.models import HomePage

from wagtail.core.models import Page, Site


class BlogTests(TestCase):
    def setUp(self):
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

        self.blog_index = BlogIndexPage(
            slug = 'blog',
            title = 'blog index title',
        )
        home.add_child(instance = self.blog_index)       

        now = datetime.utcnow()

        self.otherblog = BlogPage(
            slug = 'otherpost',
            title = 'other title',
            introduction = 'other introduction',
            body = 'other body',
            date_published = (now - timedelta(minutes = 10))
        )
        self.blog_index.add_child(instance = self.otherblog)
        self.otherblog.save

        self.prevblog = BlogPage(
            slug = 'prevpost',
            title = 'prev title',
            introduction = 'prev introduction',
            body = 'prev body',
            date_published = (now - timedelta(minutes = 5))
        )
        self.blog_index.add_child(instance = self.prevblog)
        self.prevblog.save()


        self.blog = BlogPage(
            slug = 'blogpost',
            title = 'blog title',
            introduction = 'blog introduction',
            body = 'blog body',
            first_published_at = (now + timedelta(minutes=1))
        )
        self.blog_index.add_child(instance = self.blog)
        self.blog.save()

        self.nextblog = BlogPage(
            slug = 'nextpost',
            title = 'next title',
            introduction = 'next introduction',
            body = 'next body',
            first_published_at = (now + timedelta(minutes=5))
        )
        self.blog_index.add_child(instance = self.nextblog)
        self.nextblog.save()

    def test_blog(self):
        r = self.client.get(path=self.blog_index.url)
        self.assertEqual(r.status_code, 200)

        r = self.client.get(path=self.blog.url)
        self.assertEqual(r.status_code, 200)

        self.assertIn(self.blog.title.encode(), r.content)
        self.assertIn(self.blog.introduction.encode(), r.content)
        # self.assertIn(blog.body.raw_text.encode(), r.content)
        self.assertIn(('href="%s"' % self.nextblog.url).encode(), r.content)
        self.assertIn(('href="%s"' % self.prevblog.url).encode(), r.content)
        self.assertIn(('href="%s"' % self.otherblog.url).encode(), r.content)

    def test_previous_next_links_correct(self):
        self.assertTrue(self.prevblog.date < self.blog.date)
        self.assertTrue(self.nextblog.date > self.blog.date)
        blog = BlogPage.objects.get(pk=self.blog.pk)
        self.assertEquals(self.prevblog, blog.previous)
        self.assertEquals(self.nextblog, blog.next)
