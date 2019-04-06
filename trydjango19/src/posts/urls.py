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
    url(r"^(?P<slug>[\w-]+)/$", detail, name="detail"),
    url(r"^create/$", create, name="create"),
    url(r"^(?P<slug>[\w-]+)/edit/$", update, name="update"),
    url(r"^(?P<slug>[\w-]+)/delete/$", delete, name="delete"),
)
