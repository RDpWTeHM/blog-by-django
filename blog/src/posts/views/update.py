# posts/views/update.py

from . import *


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
