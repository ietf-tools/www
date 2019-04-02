from django.conf.urls import url

from .views import status


urlpatterns = [
    url(r'^status/$', status, name='status'),
 ]
