from datetime import timedelta

import pytest
from bs4 import BeautifulSoup
from django.test import Client
from django.utils import timezone

from ietf.home.models import HomePage
from .factories import IESGStatementIndexPageFactory, IESGStatementPageFactory
from .models import IESGStatementIndexPage, IESGStatementPage

pytestmark = pytest.mark.django_db


def datefmt(value):
    return value.strftime("%d/%m/%Y")


class TestIESGStatementPage:
    @pytest.fixture(autouse=True)
    def set_up(self, home: HomePage, client: Client):
        self.home = home
        self.client = client
        self.now = timezone.now()

        self.index: IESGStatementIndexPage = IESGStatementIndexPageFactory(
            parent=self.home,
        )  # type: ignore

        self.statement: IESGStatementPage = IESGStatementPageFactory(
            parent=self.index,
            date_published=self.now,
        )  # type: ignore

    def test_index_page(self):
        response = self.client.get(path=self.index.url)
        assert response.status_code == 200
        html = response.content.decode()

        assert self.statement.title in html
        assert f'href="{self.statement.url}"' in html

    def test_statement_page(self):
        response = self.client.get(path=self.statement.url)
        assert response.status_code == 200
        html = response.content.decode()

        assert self.statement.title in html
        assert self.statement.introduction in html
        assert f'href="{self.index.url}"' in html

    def test_filtering(self):
        old1 = IESGStatementPageFactory(
            parent=self.index, date_published=self.now - timedelta(days=10)
        )
        old2 = IESGStatementPageFactory(
            parent=self.index, date_published=self.now - timedelta(days=5)
        )
        new1 = IESGStatementPageFactory(
            parent=self.index, date_published=self.now + timedelta(days=5)
        )

        def get_filtered(days_before=0, days_after=0):
            date_from = self.now + timedelta(days=days_before)
            date_to = self.now + timedelta(days=days_after)
            params = f"date_from={datefmt(date_from)}&date_to={datefmt(date_to)}"
            response = self.client.get(f"{self.index.url}?{params}", follow=True)
            assert response.status_code == 200
            html = response.content.decode()
            soup = BeautifulSoup(html, "html.parser")
            featured = soup.select("h1")[0].get_text().strip()
            others = [
                a.get_text().strip()
                for a in soup.select('aside[aria-label="Statement listing"] h2 a')
            ]
            return (featured, others)

        assert get_filtered(-10, 10) == (
            new1.title, [self.statement.title, old2.title, old1.title]
        )

        assert get_filtered(0, 10) == (new1.title, [self.statement.title])

        assert get_filtered(-10, 0) == (old2.title, [old1.title])
