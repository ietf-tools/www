import pytest
from django.test import Client

from ietf.standard.factories import IABStandardPageFactory, StandardPageFactory
from ietf.standard.models import StandardPage

from .models import HomePage, IABHomePage

pytestmark = pytest.mark.django_db


class TestHome:
    @pytest.fixture(autouse=True)
    def set_up(self, home: HomePage, client: Client):
        self.home = home
        self.client = client

    def test_homepage(self):
        response = self.client.get(path=self.home.url)
        assert response.status_code == 200
        html = response.content.decode()

        assert "<title>IETF" in html
        assert self.home.title in html
        assert self.home.heading in html
        assert self.home.introduction in html

    def test_button(self):
        page: StandardPage = StandardPageFactory(
            parent=self.home,
        )  # type: ignore
        self.home.button_text = "Homepage button text"
        self.home.button_link = page
        self.home.save(update_fields=["button_text", "button_link"])

        response = self.client.get(path=self.home.url)
        assert response.status_code == 200
        html = response.content.decode()

        assert self.home.button_text in html
        assert f'href="{page.url}"' in html


IAB_FEED_XML = """\
<?xml version="1.0" encoding="utf-8"?>
<rss xmlns:atom="http://www.w3.org/2005/Atom" version="2.0">
  <channel>
    <title/>
    <link>http://www.ietf.org/blog/</link>
    <description/>
    <atom:link href="http://www.ietf.org/blog/iab/feed/" rel="self"/>
    <language>en-gb</language>
    <lastBuildDate>Tue, 05 Mar 2024 14:46:00 +0000</lastBuildDate>
    <item>
      <title>IAB Workshop on Barriers to Internet Access of Services (BIAS)</title>
      <link>http://www.ietf.org/blog/iab-bias-workshop/</link>
      <description>The Internet Architecture Board (IAB) organizes workshops about topics of interest to the community that bring diverse experts together, raise awareness, and possibly identify the next steps that can be explored by the community. The IAB held its “Barriers for Internet Access of Services (Bias)” fully online workshop  during the week of January 15, 2024.</description>
      <dc:creator xmlns:dc="http://purl.org/dc/elements/1.1/">Dhruv Dhody</dc:creator>
      <pubDate>Tue, 05 Mar 2024 14:46:00 +0000</pubDate>
      <guid>http://www.ietf.org/blog/iab-bias-workshop/</guid>
    </item>
    <item>
      <title>Stepping towards a Sustainable Internet</title>
      <link>http://www.ietf.org/blog/eimpact-program-workshop/</link>
      <description>The IAB’s new Environmental Impacts of Internet Technology (E-Impact)  program will hold its first virtual interim meeting over two slots on February 15th and 16th 2024. These interim meetings are open to participation, and we invite all interested community members to join, participate, and contribute.</description>
      <dc:creator xmlns:dc="http://purl.org/dc/elements/1.1/">Jari Arkko, Suresh Krishnan</dc:creator>
      <pubDate>Wed, 07 Feb 2024 09:56:00 +0000</pubDate>
      <guid>http://www.ietf.org/blog/eimpact-program-workshop/</guid>
    </item>
  </channel>
</rss>
"""


class TestIABHome:
    @pytest.fixture(autouse=True)
    def set_up(self, iab_home: IABHomePage, client: Client):
        self.home = iab_home
        self.client = client

    def test_homepage(self):
        response = self.client.get(path=self.home.url)
        assert response.status_code == 200
        html = response.content.decode()

        assert "<title>IAB" in html
        assert self.home.title in html
        assert self.home.heading in html

    def test_button(self):
        page: StandardPage = IABStandardPageFactory(
            parent=self.home,
        )  # type: ignore
        self.home.button_text = "Homepage button text"
        self.home.button_link = page
        self.home.save(update_fields=["button_text", "button_link"])

        response = self.client.get(path=self.home.url)
        assert response.status_code == 200
        html = response.content.decode()

        assert self.home.button_text in html
        assert f'href="{page.url}"' in html

    def test_blog_feed(self, iab_blog_feed):
        iab_blog_feed.return_value.text = IAB_FEED_XML
        response = self.client.get(path=self.home.url)
        assert response.status_code == 200
        html = response.content.decode()

        assert "IAB Workshop on Barriers to Internet Access" in html
        assert "http://www.ietf.org/blog/iab-bias-workshop/" in html

    def test_blog_feed_error_does_not_crash_homepage(self, iab_blog_feed):
        iab_blog_feed.side_effect = RuntimeError
        response = self.client.get(path=self.home.url)
        assert response.status_code == 200
        html = response.content.decode()

        assert "IAB Workshop on Barriers to Internet Access" not in html
        assert "http://www.ietf.org/blog/iab-bias-workshop/" not in html
