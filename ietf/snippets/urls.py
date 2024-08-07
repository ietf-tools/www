from django.urls import re_path

from .views import disclaimer

urlpatterns = [
    re_path(r"^disclaimer/(\d+)/$", disclaimer, name="disclaimer"),
]
