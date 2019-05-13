# sitebuilder/views.py
import os
import sys

from django.shortcuts import render
from django.conf import settings
from django.http import Http404, HttpResponse
from django.template import Template, Context
from django.utils._os import safe_join


def testbase(request):
    return render(request, 'test.html', {})


def get_page_or_404(name):
    """Return page content as a Django template or raise 404 error"""
    PAGE_NOT_FOUND = "Page Not Found"

    try:
        file_path = safe_join(settings.SITE_PAGES_DIRECTORY, name)
    except ValueError:
        raise Http404(PAGE_NOT_FOUND)
    else:
        if not os.path.exists(file_path):
            raise Http404(PAGE_NOT_FOUND)
    with open(file_path, 'r') as f:
        page = Template(f.read())

    return page


def page(request, slug='index'):
    """Render the requested page if found."""
    file_name = "{}.html".format(slug)
    page = get_page_or_404(file_name)
    context = {
        'slug': slug,
        'buildpage': page,
    }
    return render(request, 'reprint/page.html', context)


def get_pure_page_or_404(filename):
    PAGE_NOT_FOUND = "Page Not Found"
    try:
        file_path = safe_join(settings.SITE_PAGES_DIRECTORY, filename)
        file_path += ".html"  # for django.conf.urls.url - RE
    except ValueError:
        raise Http404(PAGE_NOT_FOUND)
    else:
        if not os.path.exists(file_path):
            raise Http404(PAGE_NOT_FOUND)
    with open(file_path, 'r') as f:
        pure_page = f.read()

    return pure_page


def reprint(request, filename):
    page = get_pure_page_or_404("reprint/" + filename)
    return HttpResponse(page)


def reprint_list(request):
    # TODO: Pagination
    reprint_blog_path = safe_join(settings.SITE_PAGES_DIRECTORY, "reprint")

    def is_html(filename):
        nonlocal reprint_blog_path
        full_filepath = os.path.join(reprint_blog_path, filename)
        if os.path.isfile(full_filepath) and filename.endswith('.html'):
            return True
        return False

    files = os.listdir(reprint_blog_path)
    filenames = [_ for _ in filter(is_html, files)]

    return render(request, "list_reprint.html",
                  {"filenames": filenames})
