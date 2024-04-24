import pytest
from django.core import mail
from django.test import Client

from ietf.home.models import HomePage
from .factories import FormPageFactory
from .models import FormPage

pytestmark = pytest.mark.django_db


class TestFormPage:
    FORM_ADDRESS = "forms@example.com"

    @pytest.fixture(autouse=True)
    def set_up(self, home: HomePage, client: Client):
        self.home = home
        self.client = client

        self.form_page: FormPage = FormPageFactory(
            parent=self.home,
            to_address=self.FORM_ADDRESS,
        )  # type: ignore

    def test_form_page(self):
        response = self.client.get(path=self.form_page.url)
        assert response.status_code == 200
        html = response.content.decode()

        assert self.form_page.title in html
        assert self.form_page.intro in html

    def test_submit(self):
        response = self.client.post(self.form_page.url, {})
        assert response.status_code == 200
        assert len(mail.outbox) == 1
        message = mail.outbox[0]
        assert message.to == [self.FORM_ADDRESS]
