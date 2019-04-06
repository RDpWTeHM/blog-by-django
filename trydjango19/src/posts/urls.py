from django.conf.urls import url

from .views import (
    index,
    posts_home,
)

urlpatterns = (
    url(r"^$", index),
    url(r"^home/$", posts_home),
)
