import sys
from setuptools import setup, find_packages
from setuptools.command.test import test

def run_tests(*args):
    from inline_media.tests import run_tests, delete_tmp_dirs
    errors = run_tests()
    delete_tmp_dirs()
    if errors:
        sys.exit(1)
    else:
        sys.exit(0)

test.run_tests = run_tests

setup(
    name = "django-inline-media",
    version = "1.2",
    packages = find_packages(),
    license = "MIT",
    description = "Simple Django app that allows insertion of inline media objects in text fields, with support for rich text editor Wysihtml5.",
    long_description = "Simple Django app that allows insertion of inline media in text fields. Based on django-basic-apps/inlines, comes with two models, Picture and PictureSet, uses sorl.thumbnail, django-tagging, and the jquery plugin prettyPhoto. It also handles the insertImage command of Wysihtml5. See it in action running the demo projects.",
    author = "Daniel Rus Morales",
    author_email = "inbox@danir.us",
    maintainer = "Daniel Rus Morales",
    maintainer_email = "inbox@danir.us",
    url = "http://pypi.python.org/pypi/django-inline-media/",
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
        'Natural Language :: English',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary',
    ],
    test_suite = "dummy",
    include_package_data = True,
    package_data = {
        'inline_media': ['*.css', '*.js', '*.html']
    }
)
