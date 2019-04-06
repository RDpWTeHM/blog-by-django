from django.shortcuts import render
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

'''
page = request.GET.get('page')
try:
    contacts = paginator.page(page)
except PageNotAnInteger:
    # If page is not an integer, deliver first page.
    contacts = paginator.page(1)
except EmptyPage:
    # If page is out of range (e.g. 9999), deliver last page of results.
    contacts = paginator.page(paginator.num_pages)

return render(request, 'list.html', {'contacts': contacts})
'''


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


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    context = {
        "title": "Detail",
        "post": post,
    }
    return render(request, "posts/detail.html", context=context)


def create(request):
    postform = PostForm(request.POST or None, request.FILES or None)

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


def delete(request, pk=None):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    messages.success(request, "Successful Delete")
    return redirect("posts:list")
