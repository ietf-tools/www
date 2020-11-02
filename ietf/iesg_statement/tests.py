from django.test import Client, TestCase

from .models import IESGStatementIndexPage, IESGStatementPage
from ..home.models import HomePage

from wagtail.core.models import Page, Site

class IESGStatementPageTests(TestCase):

    def test_iesg_statement_page(self):

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

        iesg_statement_index = IESGStatementIndexPage(
            slug = 'iesg_statement_index',
            title = 'iesg statement index page title',
        )
        home.add_child(instance = iesg_statement_index)       

        iesg_statement_page = IESGStatementPage(
            slug = 'iesgstatement',
            title = 'iesg statement title',
            introduction = 'iesg statement introduction',
        )
        iesg_statement_index.add_child(instance = iesg_statement_page)

        rindex = self.client.get(path=iesg_statement_index.url or '/iesg_statement_index')
        self.assertEqual(rindex.status_code, 200)

        # r = self.client.get(path=iesg_statement_page.url or '/iesg_statement_index/iesgstatement')
        # self.assertEqual(r.status_code, 200)

        # self.assertIn(iesg_statement_page.title.encode(), r.content)
        # self.assertIn(iesg_statement_page.introduction.encode(), r.content)
        # self.assertIn(('href="%s"' % iesg_statement_index.url).encode(), r.content)
