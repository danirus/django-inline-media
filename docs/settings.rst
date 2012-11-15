.. _ref-settings:


.. index::
   single: Settings

========
Settings
========

Django-inline-media recognizes one setting:


.. index::
   single: ADMIN_IMAGES_PATH
   pair: Setting; ADMIN_IMAGES_PATH

``ADMIN_IMAGES_PATH``
=====================

**Optional**

This setting establishes the path under which Django admin images may be found.

An example::

    ADMIN_IMAGES_PATH = "%s/admin/img/admin" % STATIC_URL # Django 1.3

Defaults to ``"%s/admin/img" % settings.STATIC_URL``, the Django 1.4 admin images path.
