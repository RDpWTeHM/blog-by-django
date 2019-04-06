from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import HttpResponseRedirect
from django.contrib import messages

import os
import sys
from functools import partial

from .models import Post

from .forms import PostForm


###########
## utils ##
###########
dbg_print = partial(print, file=sys.stderr)


def index(request):
    allposts = Post.objects.all()

    context = {
        'title': "Index",
        'allposts': allposts,
    }

    return render(request, "posts/index.html",
                  context=context)


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    context = {
        "title": "Detail",
        "post": post,
    }
    return render(request, "posts/detail.html", context=context)


def create(request):
    postform = PostForm(request.POST or None)

    if postform.is_valid():
        instance = postform.save(commit=False)
        dbg_print(postform.cleaned_data.get("title"))
        instance.save()
        messages.success(request, "Successful Create")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        'title': "Create",
        'H1': 'Create Post',
        'form': postform,
    }

    return render(request, 'posts/create.html', context=context)


def update(request, pk):
    post = get_object_or_404(Post, pk=pk)

    postform = PostForm(request.POST or None, instance=post)

    if postform.is_valid():
        instance = postform.save(commit=False)
        # dbg_print(postform.cleaned_data.get("title"))
        instance.save()
        messages.success(request, "Successful Saved")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": "Update",
        "H1": "Update {}".format(post.title),
        "form": postform,
    }
    return render(request, "posts/create.html", context=context)
