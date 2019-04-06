from django.conf.urls import url

from .views import (
    index,
    detail,
)

urlpatterns = (
    url(r"^$", index, name="list"),
    url(r"^detail/$", detail, name="detail"),
)
