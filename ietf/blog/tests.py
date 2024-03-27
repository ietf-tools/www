from datetime import timedelta
from django.utils import timezone

from django.test import TestCase
from wagtail.models import Page, Site

from ietf.snippets.factories import PersonFactory

from ..home.factories import HomePageFactory
from ..home.models import HomePage
from ..snippets.models import Topic
from .factories import BlogIndexPageFactory, BlogPageFactory
from .models import BlogIndexPage, BlogPage, BlogPageAuthor, BlogPageTopic


class BlogTests(TestCase):
    def setUp(self):
        root = Page.get_first_root_node()
        self.home: HomePage = HomePageFactory(parent=root)  # type: ignore

        site = Site.objects.get()
        site.root_page = self.home
        site.save(update_fields=["root_page"])

        self.blog_index: BlogIndexPage = BlogIndexPageFactory(
            parent=self.home,
            slug="blog",
        )  # type: ignore

        now = timezone.now()

        self.other_blog_page: BlogPage = BlogPageFactory(
            parent=self.blog_index,
            date_published=(now - timedelta(minutes=10)),
        )  # type: ignore

        self.prev_blog_page: BlogPage = BlogPageFactory(
            parent=self.blog_index,
            date_published=(now - timedelta(minutes=5)),
        )  # type: ignore

        self.blog_page: BlogPage = BlogPageFactory(
            parent=self.blog_index,
            first_published_at=(now + timedelta(minutes=1)),
        )  # type: ignore

        self.next_blog_page: BlogPage = BlogPageFactory(
            parent=self.blog_index,
            first_published_at=(now + timedelta(minutes=5)),
        )  # type: ignore

        self.alice = PersonFactory(name="Alice", slug="alice")
        self.bob = PersonFactory(name="Bob", slug="bob")

        BlogPageAuthor.objects.create(page=self.other_blog_page, author=self.alice)
        BlogPageAuthor.objects.create(page=self.prev_blog_page, author=self.alice)
        BlogPageAuthor.objects.create(page=self.prev_blog_page, author=self.bob)
        BlogPageAuthor.objects.create(page=self.next_blog_page, author=self.bob)

    def test_blog(self):
        r = self.client.get(path=self.blog_index.url)
        self.assertEqual(r.status_code, 200)

        r = self.client.get(path=self.blog_page.url)
        self.assertEqual(r.status_code, 200)

        self.assertIn(self.blog_page.title.encode(), r.content)
        self.assertIn(self.blog_page.introduction.encode(), r.content)
        self.assertIn(('href="%s"' % self.next_blog_page.url).encode(), r.content)
        self.assertIn(('href="%s"' % self.prev_blog_page.url).encode(), r.content)
        self.assertIn(('href="%s"' % self.other_blog_page.url).encode(), r.content)

    def test_previous_next_links_correct(self):
        self.assertTrue(self.prev_blog_page.date < self.blog_page.date)
        self.assertTrue(self.next_blog_page.date > self.blog_page.date)
        blog = BlogPage.objects.get(pk=self.blog_page.pk)
        self.assertEqual(self.prev_blog_page, blog.previous)
        self.assertEqual(self.next_blog_page, blog.next)

    def test_author_index(self):
        alice_url = self.blog_index.reverse_subpage(
            "index_by_author", kwargs={"slug": self.alice.slug}
        )
        alice_resp = self.client.get(self.blog_index.url + alice_url)
        self.assertEqual(alice_resp.status_code, 200)
        html = alice_resp.content.decode("utf8")
        self.assertIn("<title>IETF  | Articles by Alice</title>", html)
        self.assertIn("<h1>Articles by Alice</h1>", html)
        self.assertIn(self.other_blog_page.url, html)
        self.assertIn(self.prev_blog_page.url, html)
        self.assertNotIn(self.next_blog_page.url, html)
        self.assertNotIn(self.blog_page.url, html)

    def test_blog_feed(self):
        r = self.client.get(path='/blog/feed/')
        self.assertEqual(r.status_code, 200)
        self.assertIn(self.blog_page.url.encode(), r.content)
        self.assertIn(self.other_blog_page.url.encode(), r.content)

    def test_topic_feed(self):
        iab_topic = Topic(title="iab", slug="iab")
        iab_topic.save()
        iab_bptopic = BlogPageTopic(topic=iab_topic, page=self.other_blog_page)
        iab_bptopic.save()
        self.other_blog_page.topics = [iab_bptopic, ]
        self.other_blog_page.save()
        iesg_topic = Topic(title="iesg", slug="iesg")
        iesg_topic.save()
        iesg_bptopic = BlogPageTopic(topic=iesg_topic, page=self.other_blog_page)
        iesg_bptopic.save()
        self.next_blog_page.topics = [iesg_bptopic, ]
        self.next_blog_page.save()

        r = self.client.get(path='/blog/iab/feed/')
        self.assertEqual(r.status_code, 200)
        self.assertIn(self.other_blog_page.url.encode(), r.content)
        self.assertNotIn(self.blog_page.url.encode(), r.content)
        self.assertNotIn(self.next_blog_page.url.encode(), r.content)

        r = self.client.get(path='/blog/iesg/feed/')
        self.assertEqual(r.status_code, 200)
        self.assertIn(self.next_blog_page.url.encode(), r.content)
        self.assertNotIn(self.blog_page.url.encode(), r.content)
        self.assertNotIn(self.other_blog_page.url.encode(), r.content)

    def test_author_feed(self):
        alice_url = self.blog_index.reverse_subpage(
            "feed_by_author", kwargs={"slug": self.alice.slug}
        )
        self.assertIn("/feed/", alice_url)
        alice_resp = self.client.get(self.blog_index.url + alice_url)
        self.assertEqual(alice_resp.status_code, 200)
        feed = alice_resp.content.decode("utf8")
        self.assertIn(self.other_blog_page.url, feed)
        self.assertIn(self.prev_blog_page.url, feed)
        self.assertNotIn(self.next_blog_page.url, feed)
        self.assertNotIn(self.blog_page.url, feed)

    def test_homepage(self):
        response = self.client.get(path=self.home.url)
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()

        self.assertIn(f'href="{self.blog_page.url}"', html)
        self.assertIn(self.blog_page.title, html)
