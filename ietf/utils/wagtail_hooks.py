from django.conf import settings
from django.utils.html import format_html
from wagtail import hooks
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtailorderable.modeladmin.mixins import OrderableMixin

from ietf.utils.models import MenuItem


@hooks.register("insert_editor_css")
def editor_css():
    return format_html(
        '<link rel="stylesheet" href="'
        + settings.STATIC_URL
        + 'utils/css/page_editor.css">'
    )


class MenuItemAdmin(OrderableMixin, ModelAdmin):
    model = MenuItem
    menu_order = 900
    menu_label = "Secondary Menu"
    menu_icon = "list-ul"
    add_to_settings_menu = True
    list_display = ("title",)

    ordering = ["sort_order"]


modeladmin_register(MenuItemAdmin)
