Django-inline-media
===================

Buildbot CI:
 * `Testing with Django-1.5 <http://bbot.danir.us/builders/django-inline-media-dj15>`_
 * `Testing with Django-1.4 <http://bbot.danir.us/builders/django-inline-media-dj14>`_
 * `Testing with Django-1.3 <http://bbot.danir.us/builders/django-inline-media-dj13>`_


By Daniel Rus Morales <http://danir.us/>

* http://pypi.python.org/pypi/django-inline-media/
* http://github.com/danirus/django-inline-media/

Simple Django app that allows insertion of inline media objects in text fields. Based on django-basic-apps/inlines, comes with two models, Picture and PictureSet, uses sorl.thumbnail, django-tagging, and the jquery plugin prettyPhoto.

Read the documentation at:

* `Read The Docs`_
* `Python Packages Site`_

.. _`Read The Docs`: http://readthedocs.org/docs/django-inline-media/
.. _`Python Packages Site`: http://packages.python.org/django-inline-media/

Includes a **demo project** and a limited **test suite**. If you commit code, please consider adding proper coverage (especially if it has a chance for a regression) in the test suite.

Run the tests with:  ``python setup.py test``
