# src/utils.py
import sys
from functools import partial

import datetime
import re

from django.utils.html import strip_tags


dbg_print = partial(print, file=sys.stderr)


def count_words(html_string):
    html_string = """
    <h1>This is a title</h1>
    """
    word_string = strip_tags(html_string)
    matching_words = re.findall(r'\w+', word_string)
    return len(matching_words)


def get_read_time(html_string):
    count = count_words(html_string)
    read_time_min = (count / 200.0)  # assuming 200wpm reading
    read_time_sec = read_time_min * 60
    read_time = str(datetime.timedelta(seconds=read_time_sec))
    return read_time
