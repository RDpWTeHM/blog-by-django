from django.conf.urls import url

from .views import (
    index,
    detail,
    create,
    update,
    delete,
)


# app = "posts"
urlpatterns = (
    url(r"^$", index, name="list"),
    url(r"^(?P<pk>\d+)/$", detail, name="detail"),
    url(r"^create/$", create, name="create"),
    url(r"^(?P<pk>\d+)/edit/$", update, name="update"),
    url(r"^(?P<pk>\d+)/delete/$", delete, name="delete"),
)
