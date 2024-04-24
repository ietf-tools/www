from datetime import timedelta
from bs4 import BeautifulSoup
from django.test import Client
from django.utils import timezone

import pytest

from ietf.snippets.factories import PersonFactory, TopicFactory
from ietf.home.models import HomePage
from ietf.snippets.models import Topic
from .factories import BlogIndexPageFactory, BlogPageFactory
from .models import (
    IESG_STATEMENT_TOPIC_ID,
    BlogIndexPage,
    BlogPage,
    BlogPageAuthor,
    BlogPageTopic,
)

pytestmark = pytest.mark.django_db


def datefmt(value):
    return value.strftime("%d/%m/%Y")


class TestBlog:
    @pytest.fixture(autouse=True)
    def set_up(self, home: HomePage, client: Client):
        self.home = home
        self.client = client

        self.blog_index: BlogIndexPage = BlogIndexPageFactory(
            parent=self.home,
            slug="blog",
        )  # type: ignore

        self.now = timezone.now()

        self.iab_topic: Topic = TopicFactory(title="iab")  # type: ignore
        self.iesg_topic: Topic = TopicFactory(title="iesg")  # type: ignore

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
            body__0__heading="Heading in body Streamfield",
        )  # type: ignore

        self.next_blog_page: BlogPage = BlogPageFactory(
            parent=self.blog_index,
            first_published_at=self.now + timedelta(days=5),
            topics=[BlogPageTopic(topic=self.iesg_topic)],
        )  # type: ignore

        self.alice = PersonFactory(name="Alice")
        self.bob = PersonFactory(name="Bob")

        BlogPageAuthor.objects.create(page=self.other_blog_page, author=self.alice)
        BlogPageAuthor.objects.create(page=self.prev_blog_page, author=self.alice)
        BlogPageAuthor.objects.create(page=self.prev_blog_page, author=self.bob)
        BlogPageAuthor.objects.create(page=self.next_blog_page, author=self.bob)

    def test_blog(self):
        index_response = self.client.get(path=self.blog_index.url)
        assert index_response.status_code == 200

        response = self.client.get(path=self.blog_page.url)
        assert response.status_code == 200
        html = response.content.decode()

        assert self.blog_page.title in html
        assert self.blog_page.body[0].value in html
        assert self.blog_page.introduction in html
        assert ('href="%s"' % self.next_blog_page.url) in html
        assert ('href="%s"' % self.prev_blog_page.url) in html
        assert ('href="%s"' % self.other_blog_page.url) in html

    def test_previous_next_links_correct(self):
        assert self.prev_blog_page.date < self.blog_page.date
        assert self.next_blog_page.date > self.blog_page.date
        blog = BlogPage.objects.get(pk=self.blog_page.pk)
        assert self.prev_blog_page == blog.previous
        assert self.next_blog_page == blog.next

    def test_author_index(self):
        alice_url = self.blog_index.reverse_subpage(
            "index_by_author", kwargs={"slug": self.alice.slug}
        )
        alice_resp = self.client.get(self.blog_index.url + alice_url)
        assert alice_resp.status_code == 200
        html = alice_resp.content.decode("utf8")
        assert "<title>IETF  | Articles by Alice</title>" in html
        assert "<h1>Articles by Alice</h1>" in html
        assert self.other_blog_page.url in html
        assert self.prev_blog_page.url in html
        assert self.next_blog_page.url not in html
        assert self.blog_page.url not in html

    def test_blog_feed(self):
        response = self.client.get(path="/blog/feed/")
        assert response.status_code == 200
        html = response.content.decode()

        assert self.blog_page.url in html
        assert self.other_blog_page.url in html

    def test_topic_feed(self):
        iab_response = self.client.get(path="/blog/iab/feed/")
        assert iab_response.status_code == 200
        iab_html = iab_response.content.decode()

        assert self.other_blog_page.url in iab_html
        assert self.blog_page.url not in iab_html
        assert self.next_blog_page.url not in iab_html

        ietf_response = self.client.get(path="/blog/iesg/feed/")
        assert ietf_response.status_code == 200
        ietf_html = ietf_response.content.decode()

        assert self.next_blog_page.url in ietf_html
        assert self.blog_page.url not in ietf_html
        assert self.other_blog_page.url not in ietf_html

    def test_author_feed(self):
        alice_url = self.blog_index.reverse_subpage(
            "feed_by_author", kwargs={"slug": self.alice.slug}
        )
        assert "/feed/" in alice_url
        alice_resp = self.client.get(self.blog_index.url + alice_url)
        assert alice_resp.status_code == 200
        feed = alice_resp.content.decode("utf8")
        assert self.other_blog_page.url in feed
        assert self.prev_blog_page.url in feed
        assert self.next_blog_page.url not in feed
        assert self.blog_page.url not in feed

    def test_homepage(self):
        """ The two most recent blog posts are shown on the homepage. """
        response = self.client.get(path=self.home.url)
        assert response.status_code == 200
        html = response.content.decode()

        assert f'href="{self.blog_page.url}"' in html
        assert self.blog_page.title in html

    def test_all_page(self):
        """ The /blog/all/ page shows all the published blog posts. """
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
        """
        Test the filtering of the blogs page.

        The blog page shows the most recent (filtered) post, along with a list
        of other posts that match the filter, in descending order of
        publication date.
        """

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
            self.next_blog_page.title,
            [self.blog_page.title],
        )

        assert get_filtered(-10, 0) == (
            self.prev_blog_page.title,
            [self.other_blog_page.title],
        )

        assert get_filtered(-10, 10, self.iab_topic) == (
            self.prev_blog_page.title,
            [self.other_blog_page.title],
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
