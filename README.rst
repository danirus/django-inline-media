django-inline-media
===================

|downloads|_ |TravisCI|_

.. |TravisCI| image:: https://secure.travis-ci.org/danirus/django-inline-media.png?branch=master
.. _TravisCI: https://travis-ci.org/danirus/django-inline-media
.. |downloads| image:: https://pypip.in/d/django-inline-media/badge.png
        :target: https://pypi.python.org/pypi/django-inline-media
.. _downloads: https://pypi.python.org/pypi/django-inline-media


Tested under:

* Python 3.2 and django 1.6 `builds <http://buildbot.danir.us/builders/django-inline-media-py32dj16>`_
* Python 3.2 and django 1.5.5 `builds <http://buildbot.danir.us/builders/django-inline-media-py32dj15>`_
* Python 2.7 and django 1.5.5 `builds <http://buildbot.danir.us/builders/django-inline-media-py27dj15>`_
* Python 2.7 and django 1.4.10 `builds <http://buildbot.danir.us/builders/django-inline-media-py27dj14>`_

By Daniel Rus Morales <http://danir.us/>

* http://pypi.python.org/pypi/django-inline-media/
* http://github.com/danirus/django-inline-media/

Simple django app that allows insertion of inline media objects in text fields. Based on django-basic-apps/inlines, comes with two models, Picture and PictureSet, uses sorl.thumbnail, django-tagging, and the jquery plugin prettyPhoto.

Read the documentation at:

* `Read The Docs`_
* `Python Packages Site`_

.. _`Read The Docs`: http://readthedocs.org/docs/django-inline-media/
.. _`Python Packages Site`: http://packages.python.org/django-inline-media/

Includes a **demo project** and a limited **test suite**. If you commit code, please consider adding proper coverage (especially if it has a chance for a regression) in the test suite.

Run the tests with:  ``python setup.py test``
