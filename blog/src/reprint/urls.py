# reprint/urls.py

from django.conf.urls import url

from django.http import HttpResponse

# from .views import testbase
from .views import (
    page,
    reprint_list, reprint
)


urlpatterns = [
    # url('test/', testbase, name="testbase"),

    url(r'^$', page, name='index'),

    url(r"^reprint/$", reprint_list, name='reprint_list'),
    url(r"^reprint/(?P<filename>[\s\w-]+)", reprint, name="reprint"),

    url(r'^(?P<slug>[\w-]+)/$', page, name='page'),
]
