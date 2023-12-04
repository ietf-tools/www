from datetime import timedelta
from django.utils import timezone

from django.test import TestCase
from wagtail.models import Page, Site

from ..home.models import HomePage
from ..snippets.models import Topic
from .models import BlogIndexPage, BlogPage, BlogPageTopic


class BlogTests(TestCase):
    def setUp(self):
        root = Page.get_first_root_node()

        home = HomePage(
            slug="homepageslug",
            title="home page title",
            heading="home page heading",
            introduction="home page introduction",
            request_for_comments_section_body="rfc section body",
            working_groups_section_body="wg section body",
        )

        root.add_child(instance=home)

        Site.objects.all().delete()

        Site.objects.create(
            hostname="localhost",
            root_page=home,
            is_default_site=True,
            site_name="testingsitename",
        )

        self.blog_index = BlogIndexPage(
            slug="blog",
            title="blog index title",
        )
        home.add_child(instance=self.blog_index)

        now = timezone.now()

        self.otherblog = BlogPage(
            slug="otherpost",
            title="other title",
            introduction="other introduction",
            body='[{"id": "1", "type": "rich_text", "value": "<p>other body</p>"}]',
            date_published=(now - timedelta(minutes=10)),
        )
        self.blog_index.add_child(instance=self.otherblog)
        self.otherblog.save

        self.prevblog = BlogPage(
            slug="prevpost",
            title="prev title",
            introduction="prev introduction",
            body='[{"id": "2", "type": "rich_text", "value": "<p>prev body</p>"}]',
            date_published=(now - timedelta(minutes=5)),
        )
        self.blog_index.add_child(instance=self.prevblog)
        self.prevblog.save()

        self.blog = BlogPage(
            slug="blogpost",
            title="blog title",
            introduction="blog introduction",
            body='[{"id": "3", "type": "rich_text", "value": "<p>blog body</p>"}]',
            first_published_at=(now + timedelta(minutes=1)),
        )
        self.blog_index.add_child(instance=self.blog)
        self.blog.save()

        self.nextblog = BlogPage(
            slug="nextpost",
            title="next title",
            introduction="next introduction",
            body='[{"id": "4", "type": "rich_text", "value": "<p>next body</p>"}]',
            first_published_at=(now + timedelta(minutes=5)),
        )
        self.blog_index.add_child(instance=self.nextblog)
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
        self.assertEqual(self.prevblog, blog.previous)
        self.assertEqual(self.nextblog, blog.next)

    def test_blog_feed(self):
        r = self.client.get(path='/blog/feed/')
        self.assertEqual(r.status_code, 200)
        self.assertIn(self.blog.url.encode(), r.content)
        self.assertIn(self.otherblog.url.encode(), r.content)

    def test_topic_feed(self):
        iab_topic = Topic(title="iab", slug="iab")
        iab_topic.save()
        iab_bptopic = BlogPageTopic(topic=iab_topic, page=self.otherblog)
        iab_bptopic.save()
        self.otherblog.topics = [iab_bptopic, ]
        self.otherblog.save()
        iesg_topic = Topic(title="iesg", slug="iesg")
        iesg_topic.save()
        iesg_bptopic = BlogPageTopic(topic=iesg_topic, page=self.otherblog)
        iesg_bptopic.save()
        self.nextblog.topics = [iesg_bptopic, ]
        self.nextblog.save()

        r = self.client.get(path='/blog/iab/feed/')
        self.assertEqual(r.status_code, 200)
        self.assertIn(self.otherblog.url.encode(), r.content)
        self.assertNotIn(self.blog.url.encode(), r.content)
        self.assertNotIn(self.nextblog.url.encode(), r.content)

        r = self.client.get(path='/blog/iesg/feed/')
        self.assertEqual(r.status_code, 200)
        self.assertIn(self.nextblog.url.encode(), r.content)
        self.assertNotIn(self.blog.url.encode(), r.content)
        self.assertNotIn(self.otherblog.url.encode(), r.content)
