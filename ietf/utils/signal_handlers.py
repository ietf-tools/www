from django.db.models.signals import post_delete, post_save
from wagtail.contrib.frontend_cache.utils import purge_pages_from_cache
from wagtail.models import Page, ReferenceIndex
from wagtail.signals import page_published, page_unpublished

from ietf.utils.models import MainMenuItem


def register_signal_handlers():
    def page_published_or_unpublished_handler(instance, **kwargs):
        home_page = instance.get_site().root_page
        purge_pages = set()

        if instance.pk != home_page.pk:
            parent = instance.get_parent()
            purge_pages.add(parent)

        for obj, _ in ReferenceIndex.get_grouped_references_to(instance):
            if isinstance(obj, Page):
                if obj.live:
                    purge_pages.add(obj)

            if isinstance(obj, MainMenuItem):
                purge_pages.add(home_page)

        purge_pages_from_cache(purge_pages)

    def main_menu_item_saved_or_deleted_handler(instance, **kwargs):
        home_page = instance.page.get_site().root_page
        purge_pages_from_cache({home_page})

    page_published.connect(page_published_or_unpublished_handler)
    page_unpublished.connect(page_published_or_unpublished_handler)
    post_save.connect(main_menu_item_saved_or_deleted_handler, sender=MainMenuItem)
    post_delete.connect(main_menu_item_saved_or_deleted_handler, sender=MainMenuItem)
