# posts/views/create.py

from . import *


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
