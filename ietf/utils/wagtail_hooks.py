from django.conf import settings
from django.utils.html import format_html
from wagtail import hooks
from wagtail.models import Page
from wagtail_ab_testing.events import BaseEvent
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from wagtailorderable.modeladmin.mixins import OrderableMixin

from ietf.utils.models import MenuItem


@hooks.register("insert_global_admin_css")
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


class NavigateToRegistrationWebsite(BaseEvent):
    name = "Navigate to registration website"


class NavigateToMailmanWebsite(BaseEvent):
    name = "Navigate to Mailman website"


class SubmitDonationFormEvent(BaseEvent):
    name = "Submit donation form"


@hooks.register("register_ab_testing_event_types")
def register_ab_testing_event_types():
    return {
        "navigate-registration": NavigateToRegistrationWebsite(),
        "navigate-mailman": NavigateToMailmanWebsite(),
        "submit-donation-form": SubmitDonationFormEvent(),
    }
