from operator import attrgetter

from ietf.utils.models import MainMenuItem


class MainMenu:
    def __init__(self, site):
        self.site = site

    def get_items(self):
        return MainMenuItem.objects.all().select_related("page")

    def get_introduction(self, page):
        if hasattr(page, "introduction"):
            return page.introduction

        return ""

    def get_section_links(self, section):
        for link in section.value.get("links"):
            if link.text and link.url:
                yield link

    def get_menu_item(self, item):
        main_section_links = [
            {
                "title": page.title,
                "url": item.page.get_url(current_site=self.site),
            }
            for page in item.page.get_children().live().in_menu()
        ]
        secondary_sections = [
            {
                "title": section.value.get("title"),
                "links": list(self.get_section_links(section)),
            }
            for section in item.secondary_sections
        ]
        return {
            "main_menu_item": item,
            "title": item.page.title,
            "url": item.page.get_url(current_site=self.site) if item.page.live else "",
            "introduction": self.get_introduction(item.page.specific),
            "image": item.image,
            "main_section_links": main_section_links,
            "secondary_sections": secondary_sections,
            "expandable": bool(main_section_links or secondary_sections),
        }

    def get_menu(self):
        return [
            self.get_menu_item(item)
            for item in self.get_items()
        ]


class PreviewMainMenu(MainMenu):
    def __init__(self, site, obj):
        super().__init__(site)
        self.obj = obj

    def get_items(self):
        items = [
            self.obj if item == self.obj else item
            for item in MainMenuItem.objects.all()
        ]
        if not self.obj.pk:
            items.append(self.obj)
        return sorted(items, key=attrgetter("sort_order"))


def get_iab_main_menu(site):
    def children(item):
        return item and item.get_children().live().in_menu()

    items = children(site.root_page)
    if items:
        for item in items:
            item.subitems = children(item)
    return items


def get_main_menu(site):
    if "iab" in site.hostname:
        return get_iab_main_menu(site)

    return MainMenu(site).get_menu()
