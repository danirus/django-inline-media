#!/usr/bin/env python

import imp
import sys
import os
import os.path

PRJ_PATH = os.path.abspath(os.path.curdir)
PARENT_PRJ_PATH = os.path.abspath(os.path.join(PRJ_PATH, os.pardir))
APP_PATH = os.path.abspath(os.path.join(PARENT_PRJ_PATH, os.pardir))

sys.path.insert(0, APP_PATH)
sys.path.insert(0, PARENT_PRJ_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'demo_wysihtml5.settings'

try:
    imp.find_module('settings') # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n" % __file__)
    sys.exit(1)

import settings
from sorl.thumbnail import get_thumbnail
from inline_media.models import Picture 

def do_cache_article_pics():
    pics_sizes = (
        ( 1, "250"), # article 6 uses picture  1 with 250px width
        ( 2, "350"), # article 5 uses picture  2 with 350px width
        ( 6, "250"), # article 4 uses picture  6 with 250px width
        (18, "350"), # article 3 uses picture 18 with 350px width
        (16, "350"), # article 2 uses picture 16 with 350px width
        (13, "350"), # article 1 uses picture 13 with 350px width
    )
    
    for picid, size in pics_sizes:
        pic = Picture.objects.get(pk=picid)
        get_thumbnail(pic.picture.file, size)


if __name__ == '__main__':
    do_cache_article_pics()
