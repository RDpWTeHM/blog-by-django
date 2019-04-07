# posts/views/delete.py

from . import *


def delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    post = get_object_or_404(Post, slug=slug)
    post.delete()
    messages.success(request, "Successful Delete")
    return redirect("posts:list")
