from django.core import mail
from django.test import TestCase
from wagtail.models import Page, Site

from ..home.factories import HomePageFactory
from ..home.models import HomePage
from .factories import FormPageFactory
from .models import FormPage


class FormPageTests(TestCase):
    FORM_ADDRESS = "forms@example.com"

    def setUp(self):
        root = Page.get_first_root_node()
        self.home: HomePage = HomePageFactory(parent=root)  # type: ignore

        site = Site.objects.get()
        site.root_page = self.home
        site.save(update_fields=["root_page"])

        self.form_page: FormPage = FormPageFactory(
            parent=self.home,
            to_address=self.FORM_ADDRESS,
        )  # type: ignore

    def test_form_page(self):
        response = self.client.get(path=self.form_page.url)
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()

        self.assertIn(self.form_page.title, html)
        self.assertIn(self.form_page.intro, html)

    def test_submit(self):
        response = self.client.post(self.form_page.url, {})
        assert response.status_code == 200
        assert len(mail.outbox) == 1
        message = mail.outbox[0]
        assert message.to == [self.FORM_ADDRESS]
