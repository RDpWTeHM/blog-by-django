# posts/views/detail.py

from . import *


def detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.draft or post.publish > timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404

    # best thing here - initial Foreign thing at the get before the post
    initial4comment = {
        'content_type': post.get_content_type,
        'object_id': post.id,
    }
    comment_form = CommentForm(request.POST or None, initial=initial4comment)
    if comment_form.is_valid():
        dbg_print(comment_form.cleaned_data)
        c_type = comment_form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = comment_form.cleaned_data.get("object_id")
        content_data = comment_form.cleaned_data.get("content")

        _, created = Comment.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=obj_id,
            content=content_data,
        )
        if created:
            dbg_print("It works!")

    context = {
        "title": "Detail",
        "post": post,
        # 'comments': Comment.objects.filter_by_instance(post),
        'comment_form': comment_form,
    }
    return render(request, "posts/detail.html", context=context)
