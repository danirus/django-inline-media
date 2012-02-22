.. _ref-settings:

========
Settings
========

Django-inline-media recognizes one setting:


``INLINE_MEDIA_STORAGE``
========================

**Optional**

This setting establishes the storage object in use for the *ImageField*, in the inline_media *Picture* model.

An example::

     INLINE_MEDIA_STORAGE = FileSystemStorage(tempfile.mkdtemp())

Defaults to ``django.core.files.storage.default_storage``
