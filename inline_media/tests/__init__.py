import os
import shutil
import six
import sys


def setup_django_settings():
    if os.environ.get("DJANGO_SETTINGS_MODULE", False):
        return
    os.chdir(os.path.join(os.path.dirname(__file__), ".."))
    sys.path.insert(0, os.getcwd())
    os.environ["DJANGO_SETTINGS_MODULE"] = "tests.settings"


def delete_tmp_dirs():
    from django.conf import settings
    try:
        shutil.rmtree(os.path.join(settings.MEDIA_ROOT, 'pictures'))
        shutil.rmtree(os.path.join(settings.MEDIA_ROOT, 'cache'))
    except OSError as exc:
        if exc.errno != 2:
            six.reraise(exc)
