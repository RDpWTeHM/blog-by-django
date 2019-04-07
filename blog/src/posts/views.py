from django.shortcuts import render, Http404
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages

from django.utils import timezone

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Q

import os
import sys
from functools import partial

from .models import Post

from .forms import PostForm
# from django.contrib.contenttypes.models import ContentType
from comments.models import Comment


###########
## utils ##
###########
dbg_print = partial(print, file=sys.stderr)


def index(request):  # posts list
    if request.user.is_staff or request.user.is_superuser:
        allposts = Post.objects.all()
    else:
        allposts = Post.objects.active()

    if request.GET.get('q', None):
        key = request.GET.get('q')
        allposts = allposts.filter(
            Q(title__icontains=key) |
            Q(content__icontains=key) |
            Q(user__first_name__icontains=key) |
            Q(user__last_name__icontains=key)
        ).distinct()

    paginator = Paginator(allposts, 5)  # Show 25 contacts per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
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
        'page_request_var': page_request_var,
        'today': timezone.now().date(),
    }

    return render(request, "posts/index.html",
                  context=context)


def detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.draft or post.publish > timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404

    context = {
        "title": "Detail",
        "post": post,
        # 'comments': Comment.objects.filter_by_instance(post),
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
