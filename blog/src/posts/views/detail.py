# posts/views/detail.py
"""
functional:
  - display post detail
  - logged-in user could comment the post(create comment)

"""

from django.contrib.contenttypes.models import ContentType

from comments.models import Comment
from comments.forms import CommentForm

from . import *


# TODO: Refactoring to class later
# data for view

def get_initail4comment(instance: 'POST') -> dict:
    return {
        'content_type': instance.get_content_type,
        'object_id': instance.id,
    }


def get_context(instance: 'POST') -> dict:
    '''comment part(only for post(article))
       or, can consider as this context for render basic post detail page
    '''
    return {
        "title": "Detail",
        "post": instance,
    }


def comment_handler(request, instance: 'Post'):
    # best thing here - initial Foreign thing at the get before the post
    comment_form = CommentForm(
        request.POST or None,
        initial=get_initail4comment(instance))
    if not comment_form.is_valid():
        context = get_context(instance=instance)
        context['comment_form'] = comment_form
        resp = render(request, "posts/detail.html", context=context)
    else:
        dbg_print(comment_form.cleaned_data)

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
        except TypeError:
            parent_obj = None

        new_comment, created = Comment.objects.get_or_create(
            user=request.user, content_type=content_type, object_id=obj_id,
            content=content_data,
            parent=parent_obj,
        )
        if created:
            dbg_print("It works!")  # maybe add 'notify' function later, later

        resp = HttpResponseRedirect(
            new_comment.content_object.get_absolute_url())

    return resp


def detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.draft or post.publish > timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404

    if request.method == 'POST':
        '''support comment'''
        if not request.user.is_active:
            raise Http404("login first!")
        else:
            return comment_handler(request, instance=post)

    elif request.method == 'GET':
        context = get_context(instance=post)

        # support comment
        # 'comments': Comment.objects.filter_by_instance(post),
        context['comment_form'] = CommentForm(initial=get_initail4comment(post))

        return render(request, "posts/detail.html", context=context)
