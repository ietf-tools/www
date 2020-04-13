from django.urls import reverse

from wagtail.core import hooks
from wagtail.admin.menu import MenuItem


@hooks.register('register_admin_menu_item')
def register_resource_menu_item():
    return MenuItem('Documentation',
                    reverse('django-admindocs-docroot'),
                    classnames='icon icon-folder-inverse',
                    order=10000)


