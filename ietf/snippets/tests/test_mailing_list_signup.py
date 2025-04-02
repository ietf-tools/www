import pytest
from bs4 import BeautifulSoup
from django.test import Client
from django.urls import reverse

from ietf.home.models import HomePage
from ietf.snippets.factories import MailingListSignupFactory, WorkingGroupFactory
from ietf.standard.factories import StandardPageFactory

pytestmark = pytest.mark.django_db


def test_disclaimer(client: Client, home: HomePage):
    """
    The "note well" disclaimer is a page that is shown when a user clicks on a
    mailing list link. It displays an informative text, and the "next" button
    is a link to the actual mailing list.
    """
    snippet = MailingListSignupFactory()
    page = StandardPageFactory(parent=home, mailing_list_signup=snippet)

    page_response = client.get(page.url)
    assert page_response.status_code == 200
    page_html = page_response.content.decode()
    page_soup = BeautifulSoup(page_html, "html.parser")
    [link] = page_soup.select(".mailing_list_signup__container a")
    disclaimer_url = reverse("disclaimer", args=[snippet.pk])
    assert link.attrs["href"] == disclaimer_url

    disclaimer_response = client.get(disclaimer_url)
    assert disclaimer_response.status_code == 200
    disclaimer_html = disclaimer_response.content.decode()
    disclaimer_soup = BeautifulSoup(disclaimer_html, "html.parser")

    assert 'See <a href="https://github.com/ietf/note-well/">' in disclaimer_html
    link = disclaimer_soup.select(".body .container a")[-1]
    assert "I understand" in link.get_text()
    assert link.attrs["href"] == snippet.sign_up


def test_link_mailto():
    snippet = MailingListSignupFactory(sign_up="foo@example.com")
    assert snippet.link == "mailto:foo@example.com"


def test_link_working_group():
    working_group = WorkingGroupFactory()
    snippet = MailingListSignupFactory(sign_up="", working_group=working_group)
    assert snippet.link == working_group.list_subscribe
