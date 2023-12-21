from django.conf import settings
from django.utils.html import format_html
from wagtail import hooks
from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail.snippets.models import register_snippet
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from wagtailorderable.modeladmin.mixins import OrderableMixin

from ietf.utils.models import MainMenuItem, SecondaryMenuItem


@hooks.register("insert_global_admin_css")
def editor_css():
    return format_html(
        '<link rel="stylesheet" href="'
        + settings.STATIC_URL
        + 'utils/css/page_editor.css">'
    )


class MainMenuViewSet(SnippetViewSet):
    list_display = [
        "__str__",
        "sort_order",
    ]


register_snippet(MainMenuItem, viewset=MainMenuViewSet)


class MenuItemAdmin(OrderableMixin, ModelAdmin):
    model = SecondaryMenuItem
    menu_order = 900
    menu_label = "Secondary Menu"
    menu_icon = "list-ul"
    add_to_settings_menu = True
    list_display = ("title",)

    ordering = ["sort_order"]


modeladmin_register(MenuItemAdmin)
