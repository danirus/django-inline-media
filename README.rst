django-inline-media
===================

|pypi| |travis| |coveralls|

.. |travis| image:: https://secure.travis-ci.org/danirus/django-inline-media.png?branch=master
    :target: https://travis-ci.org/danirus/django-inline-media
.. |pypi| image:: https://badge.fury.io/py/django-inline-media.png
    :target: http://badge.fury.io/py/django-inline-media
.. |coveralls| image:: https://coveralls.io/repos/danirus/django-inline-media/badge.png?branch=master
    :target: https://coveralls.io/r/danirus/django-inline-media?branch=master


A reusable Django app that allows insertion of inline media objects in text fields. Based on django-basic-apps/inlines, comes with two models, Picture and PictureSet, uses sorl.thumbnail, django-taggit, and the jquery plugin prettyPhoto.

1. Inserts pictures and collection of pictures into your texts using the ``TextAreaWithInlines`` widget.

2. Positions media content at different places and sizes (mini/small/medium/large at left/right or full at the left/center/right).

3. Facilitates administration with thumbnails and search by tags, author and license.

4. Shows a customised control to insert media content in text fields.

5. Uses jquery `prettyPhoto <http://www.no-margin-for-errors.com/projects/prettyphoto-jquery-lightbox-clone/>`_ to show pictures and galleries when clicking on them.

Demo site and tests working in Django 1.8, 1.9 and 1.10 under Python 2.7 and Python 3 (3.2, 3.4, 3.5 and 3.6).


The following sample shows a centered inline picture set inserted in a text, on mouseover event the first 3 photos unfold:

.. image:: https://github.com/danirus/django-inline-media/blob/master/docs/images/cover.png

Read the documentation at:

* `Read The Docs`_
* `Python Packages Site`_

.. _`Read The Docs`: http://readthedocs.org/docs/django-inline-media/
.. _`Python Packages Site`: http://packages.python.org/django-inline-media/

Includes a **demo project** and a limited **test suite**. If you commit code, please consider adding proper coverage (especially if it has a chance for a regression) in the test suite.

Run tests with:  ``tox``
