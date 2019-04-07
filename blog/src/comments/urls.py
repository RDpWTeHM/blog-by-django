from django.conf.urls import url

from .views import comment_thread, comment_delete


# app = "posts"
urlpatterns = (
    # url(r"^$", index, name="list"),
    # url(r"^create/$", create, name="create"),  # bug with slug
    url(r"^(?P<pk>[\d+])/$", comment_thread, name="thread"),
    # url(r"^(?P<slug>[\w-]+)/edit/$", update, name="update"),)
    url(r"^(?P<pk>[\d+])/delete/$", comment_delete, name="delete"),
)
