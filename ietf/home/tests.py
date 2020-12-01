from django.test import TestCase

from .models import HomePage, RequestForCommentsSectionLinks, WorkingGroupsSectionLinks
from ..blog.models import BlogPage, BlogIndexPage
from ..snippets.models import RFC, WorkingGroup

from wagtail.core.models import Page, Site

class HomeTests(TestCase):

    def test_homepage(self):

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

        self.assertEqual(HomePage.objects.count(), 1)

        Site.objects.all().delete()

        Site.objects.create(
            hostname='localhost',
            root_page = home,
            is_default_site=True,
            site_name='testingsitename',
        )

        blogindex = BlogIndexPage(
            slug = 'blog',
            title = 'blog index title',
        )
        home.add_child(instance = blogindex)       

        blog = BlogPage(
            slug = 'blogpost',
            title = 'blog title',
            introduction = 'blog introduction',
            body = 'blog body'
        )
        blogindex.add_child(instance = blog)

        home.button_text = 'blog button text'
        home.button_link = blog
        home.save()

        r = self.client.get(path=home.url)
        self.assertEqual(r.status_code, 200)
        self.assertIn(home.title.encode(), r.content)
        self.assertIn(home.heading.encode(), r.content)
        self.assertIn(home.introduction.encode(), r.content)
        self.assertIn(home.button_text.encode(), r.content)
        self.assertIn(('href="%s"' % blog.url).encode(), r.content)


        # other_page = BlogPage.objects.create(
        #     introduction = 'blog introduction',
        #     title='blog title',
        #     slug='blog-slug',
        # )

        # home = HomePage.objects.create(
        #     heading = 'homepage heading',
        #     introduction = 'homepage introduction',
        #     #main_image = TODO,
        #     button_text = 'homepage button text',
        #     button_link_id = other_page,
        # )

        # r = self.client.get(url=home.url_path)
        # self.assertEqual(r.status_code, 200)



