from django.conf.urls import url

from .views import chosen, chooser

app_name = 'snippetlink'

urlpatterns = [
    url(r'^chooser/(?P<snippet_type>[\w-]+)/$', chooser, name='chooser'),
    url(r'^chosen/(?P<snippet_type>[\w-]+)/(?P<item_id>\d+)$', chosen, name='chosen'),
]
