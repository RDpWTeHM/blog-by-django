# posts/views/__init__.py
from django.shortcuts import render, Http404
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages

from django.utils import timezone

import os
import sys
from functools import partial

from posts.models import Post

from posts.forms import PostForm


###########
## utils ##
###########
dbg_print = partial(print, file=sys.stderr)
