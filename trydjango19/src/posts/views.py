from django.shortcuts import render, Http404
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import os
import sys
from functools import partial

from .models import Post

from .forms import PostForm


###########
## utils ##
###########
dbg_print = partial(print, file=sys.stderr)


def index(request):  # posts list
    allposts = Post.objects.all()
    paginator = Paginator(allposts, 5)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        qs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        qs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        qs = paginator.page(paginator.num_pages)

    context = {
        'title': "Index",
        'posts_list': qs,
    }

    return render(request, "posts/index.html",
                  context=context)


def detail(request, slug):
    post = get_object_or_404(Post, slug=slug)

    context = {
        "title": "Detail",
        "post": post,
    }
    return render(request, "posts/detail.html", context=context)


def create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    # if not request.user.is_authenticated():
        # raise Http404
    postform = PostForm(request.POST or None, request.FILES or None)

    if postform.is_valid():
        instance = postform.save(commit=False)
        instance.user = request.user
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


def update(request, slug):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    post = get_object_or_404(Post, slug=slug)

    postform = PostForm(request.POST or None,
                        request.FILES or None, instance=post)

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


def delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    post = get_object_or_404(Post, slug=slug)
    post.delete()
    messages.success(request, "Successful Delete")
    return redirect("posts:list")
