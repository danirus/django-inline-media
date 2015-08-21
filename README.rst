django-inline-media
===================

|pypi| |travis| |coveralls|

.. |travis| image:: https://secure.travis-ci.org/danirus/django-inline-media.png?branch=master
    :target: https://travis-ci.org/danirus/django-inline-media
.. |pypi| image:: https://badge.fury.io/py/django-inline-media.png
    :target: http://badge.fury.io/py/django-inline-media
.. |coveralls|: image:: https://coveralls.io/repos/danirus/django-inline-media/badge.png?branch=master
    :target: https://coveralls.io/r/danirus/django-inline-media?branch=master


A reusable Django app that allows insertion of inline media objects in text fields. Based on django-basic-apps/inlines, comes with two models, Picture and PictureSet, uses sorl.thumbnail, django-taggit, and the jquery plugin prettyPhoto.

* Tested under Python 2.7 and 3.4, Django 1.7 and 1.8.
* Django-inline-media v1.2 is compatible with Django 1.4 - Django 1.6 

Read the documentation at:

* `Read The Docs`_
* `Python Packages Site`_

.. _`Read The Docs`: http://readthedocs.org/docs/django-inline-media/
.. _`Python Packages Site`: http://packages.python.org/django-inline-media/

Includes a **demo project** and a limited **test suite**. If you commit code, please consider adding proper coverage (especially if it has a chance for a regression) in the test suite.

Run tests with:  ``tox``
