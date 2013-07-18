import os
import shutil
import six
import sys
import unittest


def setup_django_settings():
    os.chdir(os.path.join(os.path.dirname(__file__), ".."))
    sys.path.insert(0, os.getcwd())
    os.environ["DJANGO_SETTINGS_MODULE"] = "tests.settings"


def run_tests():
    if not os.environ.get("DJANGO_SETTINGS_MODULE", False):
        setup_django_settings()

    from django.conf import settings
    from django.test.utils import get_runner

    TestRunner = get_runner(settings)
    test_suite = TestRunner(verbosity=2, interactive=True, failfast=False)
    return test_suite.run_tests(["inline_media"])
    

def delete_tmp_dirs():
    from django.conf import settings
    try:
        shutil.rmtree(os.path.join(settings.MEDIA_ROOT, 'pictures'))
        shutil.rmtree(os.path.join(settings.MEDIA_ROOT, 'cache'))
    except OSError as exc:
        if exc.errno != 2:
            six.reraise(e)


def suite():
    if not os.environ.get("DJANGO_SETTINGS_MODULE", False):
        setup_django_settings()
    else:
        from django.db.models.loading import load_app
        from django.conf import settings
        settings.INSTALLED_APPS = settings.INSTALLED_APPS + ['inline_media.tests',]
        map(load_app, settings.INSTALLED_APPS)

    from inline_media.tests import (test_fields, test_models, 
                                    test_parser, test_widgets,
                                    test_conf, test_templates,
                                    test_utils)

    testsuite = unittest.TestSuite([
        unittest.TestLoader().loadTestsFromModule(test_conf),
        unittest.TestLoader().loadTestsFromModule(test_fields),
        unittest.TestLoader().loadTestsFromModule(test_models),
        unittest.TestLoader().loadTestsFromModule(test_parser),
        unittest.TestLoader().loadTestsFromModule(test_widgets),
        unittest.TestLoader().loadTestsFromModule(test_templates),
        unittest.TestLoader().loadTestsFromModule(test_utils),
    ])
    return testsuite


if __name__ == "__main__":
    run_tests()
