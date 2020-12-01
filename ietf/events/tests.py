from django.test import TestCase

from .models import EventListingPage, EventPage
from ..home.models import HomePage

from wagtail.core.models import Page, Site

class EventPageTests(TestCase):

    def test_event_page(self):

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

        eventlisting = EventListingPage(
            slug = 'eventlisting',
            title = 'event listing page title',
            introduction = 'event listing page introduction'
        )
        home.add_child(instance = eventlisting)       

        eventpage = EventPage(
            slug = 'event',
            title = 'event title',
            introduction = 'event introduction',
        )
        eventlisting.add_child(instance = eventpage)

        rindex = self.client.get(path=eventlisting.url)
        self.assertEqual(rindex.status_code, 200)

        r = self.client.get(path=eventpage.url)
        self.assertEqual(r.status_code, 200)

        self.assertIn(eventpage.title.encode(), r.content)
        self.assertIn(eventpage.introduction.encode(), r.content)
        self.assertIn(('href="%s"' % eventlisting.url).encode(), r.content)
