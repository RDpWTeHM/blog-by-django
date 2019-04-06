from django.conf.urls import url

from .views import (
    index,
    detail,
    create,
    update,
)


# app = "posts"
urlpatterns = (
    url(r"^$", index, name="list"),
    url(r"^(?P<pk>\d+)/$", detail, name="detail"),
    url(r"^create/$", create, name="create"),
    url(r"^(?P<pk>\d+)/update/$", update, name="update"),
)
