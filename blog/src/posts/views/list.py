# posts/views/list.py

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from . import *


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
