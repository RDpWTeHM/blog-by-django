# comments/views.py
"""
"""

from django.shortcuts import render, get_object_or_404, Http404
from django.http import HttpResponseRedirect
from django.http import HttpResponse

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType

# import os
# import sys

from .models import Comment
from .forms import CommentForm


######################
#  utility function  #
######################
from utils import dbg_print


def get_initail4comment(instance: 'Comment') -> dict:
    return {
        'content_type': instance.content_type,
        'object_id': instance.object_id,
    }


def comment_thread(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404("login first!")

    obj = get_object_or_404(Comment, pk=pk)
    if not obj.is_parent:
        obj = obj.parent

    comment_form = CommentForm(
        request.POST or None,
        initial=get_initail4comment(obj))
    if comment_form.is_valid():
        # dbg_print(comment_form.cleaned_data)

        c_type = comment_form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = comment_form.cleaned_data.get("object_id")
        content_data = comment_form.cleaned_data.get("content")
        try:
            parent_id = int(request.POST.get("parent_id"))
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()
            else:
                raise ValueError("parent_qs doesn't exist")
        except ValueError:
            parent_obj = None

        new_comment, created = Comment.objects.get_or_create(
            user=request.user, content_type=content_type, object_id=obj_id,
            content=content_data,
            parent=parent_obj,
        )
        if created:
            dbg_print("It works!")  # maybe add 'notify' function later, later

        return HttpResponseRedirect(
            new_comment.content_object.get_absolute_url())

    form = comment_form

    context = {
        'comment': obj,
        'comment_form': form,
    }
    return render(request, "comment_thread.html", context=context)


def comment_delete(request, pk):
    try:
        obj = Comment.objects.get(pk=pk)
    except Comment.DoesNotExist as err:
        raise Http404(err)

    if obj.user != request.user:  # only can delete own-self
        response = HttpResponse("<h1>You have not permission to do this!</h1>")
        response.status_code = 403
        return response

    if request.method == 'POST':
        parent_obj_url = obj.content_object.get_absolute_url()
        obj.delete()
        messages.success(request, "This has been delete")
        return HttpResponseRedirect(parent_obj_url)

    context = {
        'title': "Confirm Delete",
        'object': obj,
    }

    return render(request, "confirm_delete.html", context=context)
