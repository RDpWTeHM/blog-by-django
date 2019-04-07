from django.conf.urls import url

from .views.create import create
from .views.update import update
from .views.list import index
from .views.detail import detail
from .views.delete import delete


# app = "posts"
urlpatterns = (
    url(r"^$", index, name="list"),
    url(r"^create/$", create, name="create"),  # bug with slug
    url(r"^(?P<slug>[\w-]+)/$", detail, name="detail"),
    url(r"^(?P<slug>[\w-]+)/edit/$", update, name="update"),
    url(r"^(?P<slug>[\w-]+)/delete/$", delete, name="delete"),
)
