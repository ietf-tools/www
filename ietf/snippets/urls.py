from django.conf.urls import url

from .views import disclaimer


urlpatterns = [
    url(r'^disclaimer/(\d+)/$', disclaimer, name='disclaimer'),
 ]
