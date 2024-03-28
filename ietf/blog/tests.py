from datetime import timedelta
from bs4 import BeautifulSoup
from django.utils import timezone

from django.test import TestCase
from wagtail.models import Page, Site

from ietf.snippets.factories import PersonFactory, TopicFactory

from ..home.factories import HomePageFactory
from ..home.models import HomePage
from ..snippets.models import Topic
from .factories import BlogIndexPageFactory, BlogPageFactory
from .models import IESG_STATEMENT_TOPIC_ID, BlogIndexPage, BlogPage, BlogPageAuthor, BlogPageTopic


def datefmt(value):
    return value.strftime("%d/%m/%Y")


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

        self.now = timezone.now()

        self.iab_topic: Topic = TopicFactory(title="iab", slug="iab")  # type: ignore
        self.iesg_topic: Topic = TopicFactory(title="iesg", slug="iesg")  # type: ignore

        self.other_blog_page: BlogPage = BlogPageFactory(
            parent=self.blog_index,
            date_published=self.now - timedelta(days=10),
            topics=[BlogPageTopic(topic=self.iab_topic)],
        )  # type: ignore

        self.prev_blog_page: BlogPage = BlogPageFactory(
            parent=self.blog_index,
            date_published=self.now - timedelta(days=5),
            topics=[BlogPageTopic(topic=self.iab_topic)],
        )  # type: ignore

        self.blog_page: BlogPage = BlogPageFactory(
            parent=self.blog_index,
            first_published_at=self.now + timedelta(days=1),
        )  # type: ignore

        self.next_blog_page: BlogPage = BlogPageFactory(
            parent=self.blog_index,
            first_published_at=self.now + timedelta(days=5),
            topics=[BlogPageTopic(topic=self.iesg_topic)],
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
        r = self.client.get(path="/blog/feed/")
        self.assertEqual(r.status_code, 200)
        self.assertIn(self.blog_page.url.encode(), r.content)
        self.assertIn(self.other_blog_page.url.encode(), r.content)

    def test_topic_feed(self):
        r = self.client.get(path="/blog/iab/feed/")
        self.assertEqual(r.status_code, 200)
        self.assertIn(self.other_blog_page.url.encode(), r.content)
        self.assertNotIn(self.blog_page.url.encode(), r.content)
        self.assertNotIn(self.next_blog_page.url.encode(), r.content)

        r = self.client.get(path="/blog/iesg/feed/")
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

    def test_all_page(self):
        response = self.client.get(f"{self.blog_index.url}all/")
        assert response.status_code == 200
        html = response.content.decode()
        soup = BeautifulSoup(html, "html.parser")
        links = [a.get_text().strip() for a in soup.select("main table a")]
        assert links == [
            self.next_blog_page.title,
            self.blog_page.title,
            self.prev_blog_page.title,
            self.other_blog_page.title,
        ]

    def test_filtering(self):
        def get_filtered(days_before=0, days_after=0, topic=None):
            date_from = self.now + timedelta(days=days_before)
            date_to = self.now + timedelta(days=days_after)
            params = f"date_from={datefmt(date_from)}&date_to={datefmt(date_to)}"
            if topic:
                params += f"&topic={topic.pk}"
            response = self.client.get(f"{self.blog_index.url}?{params}", follow=True)
            assert response.status_code == 200
            html = response.content.decode()
            soup = BeautifulSoup(html, "html.parser")
            featured = soup.select("h1")[0].get_text().strip()
            others = [
                a.get_text().strip()
                for a in soup.select('aside[aria-label="Blog listing"] h2 a')
            ]
            return (featured, others)

        assert get_filtered(-10, 10) == (
            self.next_blog_page.title,
            [
                self.blog_page.title,
                self.prev_blog_page.title,
                self.other_blog_page.title,
            ],
        )

        assert get_filtered(0, 10) == (
            self.next_blog_page.title, [self.blog_page.title]
        )

        assert get_filtered(-10, 0) == (
            self.prev_blog_page.title, [self.other_blog_page.title]
        )

        assert get_filtered(-10, 10, self.iab_topic) == (
            self.prev_blog_page.title, [self.other_blog_page.title]
        )

    def test_iesg_statements_redirect(self):
        params = "&".join(
            [
                f"primary_topic={IESG_STATEMENT_TOPIC_ID}",
                f"date_from={datefmt(self.now + timedelta(days=-10))}",
                f"date_to={datefmt(self.now + timedelta(days=10))}",
                f"secondary_topic={self.iab_topic.pk}",
            ]
        )
        response = self.client.get(f"{self.blog_index.url}?{params}")
        new_params = "&".join(
            [
                f"topic={self.iab_topic.pk}",
                f"date_from={datefmt(self.now + timedelta(days=-10))}",
                f"date_to={datefmt(self.now + timedelta(days=10))}",
            ]
        )
        assert response.status_code == 302
        assert response.url == f"/about/groups/iesg/statements?{new_params}"
