from django.shortcuts import render
from django.http import HttpResponse


def posts_home(request):
    return HttpResponse("<h1>Hello World</h1>")
