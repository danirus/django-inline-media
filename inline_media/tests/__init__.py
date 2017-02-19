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


def run_tests():
    if not os.environ.get("DJANGO_SETTINGS_MODULE", False):
        setup_django_settings()

    import django
    from django.conf import settings
    from django.test.utils import get_runner

    if django.VERSION[1] >= 7:  # Django 1.7.x or above
        django.setup()
        runner = get_runner(settings,
                            "django.test.runner.DiscoverRunner")
    else:
        runner = get_runner(settings,
                            "django.test.simple.DjangoTestSuiteRunner")
    test_suite = runner(verbosity=2, interactive=True, failfast=False)
    results = test_suite.run_tests(["inline_media"])
    delete_tmp_dirs()
    return results


def delete_tmp_dirs():
    from django.conf import settings
    try:
        shutil.rmtree(os.path.join(settings.MEDIA_ROOT, 'pictures'))
        shutil.rmtree(os.path.join(settings.MEDIA_ROOT, 'cache'))
    except OSError as exc:
        if exc.errno != 2:
            six.reraise(exc)
