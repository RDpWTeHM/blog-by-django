from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .models import Post


def index(request):
    allposts = Post.objects.all()

    context = {
        'title': "Index",
        'allposts': allposts,
    }

    return render(request, "posts/index.html",
                  context=context)


def detail(request):
    post = get_object_or_404(Post, pk=1)

    context = {
        "title": "Detail",
        "post": post,
    }
    return render(request, "posts/detail.html", context=context)
