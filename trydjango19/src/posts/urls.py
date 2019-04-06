from django.conf.urls import url

from .views import (
    index,
    detail,
)

urlpatterns = (
    url(r"^$", index, name="list"),
    url(r"^(?P<pk>\d+)/$", detail, name="detail"),
)
