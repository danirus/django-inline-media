.. _ref-settings:

========
Settings
========

Django-inline-media recognizes one setting:


``ADMIN_IMAGES_PATH``
=====================

**Optional**

This setting establishes the path under which Django admin images may be found.

An example::

    ADMIN_IMAGES_PATH = "%s/admin/img/admin" % STATIC_URL # Django 1.3

Defaults to ``"%s/admin/img" % settings.STATIC_URL``, the Django 1.4 admin images path.


``INLINE_MEDIA_STORAGE``
========================

**Optional**

This setting establishes the storage object in use for the *ImageField*, in the inline_media *Picture* model.

An example::

     INLINE_MEDIA_STORAGE = FileSystemStorage(tempfile.mkdtemp())

Defaults to ``django.core.files.storage.default_storage``

