from django.contrib.syndication.views import Feed
from django.db.models.functions import Coalesce
from ..blog.models import BlogPage
from ..utils.models import FeedSettings


class BlogFeed(Feed):
    link = "/blog/"

    def __call__(self, request, *args, **kwargs):
        settings = FeedSettings.for_site(request.site)
        self.title = settings.blog_feed_title
        self.description = settings.blog_feed_description
        return super().__call__(request, *args, **kwargs)

    def items(self):
        return BlogPage.objects.live().annotate(
            d=Coalesce('date_published', 'first_published_at')).order_by('-d')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.introduction

    def item_link(self, item):
        return item.get_full_url()

    def item_author_name(self, item):
        return ", ".join([a.author.name for a in item.authors.all()])

    def item_pubdate(self, item):
        return item.date
