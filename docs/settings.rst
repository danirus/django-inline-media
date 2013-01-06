.. _ref-settings:


.. index::
   single: Settings

========
Settings
========

Django-inline-media recognizes four setting:


.. index::
   single: INLINE_MEDIA_CUSTOM_SIZES
   pair: Setting; INLINE_MEDIA_CUSTOM_SIZES

``INLINE_MEDIA_CUSTOM_SIZES``
=============================

**Optional**

This setting defines custom sizes used in inline_media templates. Each ``<inline>`` element has an ``inline_type`` attribute that refers to an **app_label.model**, and a ``class`` attribute that defines the **size and alignment** of the inline element. 

``INLINE_MEDIA_CUSTOM_SIZES`` is a 2-level depth dictionary. The first level contains ``inline_types`` with **app_label.model** pairs as keys.  The second level contains ``class`` values as keys and values as geometries. 

When the value is just an **int**, it represents the **width** of the thumbnail. When the value is a **tuple** it represents the **(width, height)** of the thumbnail. If the value is something else the size is not being used in the corresponding template. It is the case of the template 'inline_media/inline_media.picture.full.html', distributed with this app.

It defaults to::

    INLINE_MEDIA_CUSTOM_SIZES = { 
                                  'inline_media.picture':
                                      { 
                                        'mini': 80,
                                        'small': 150,
                                        'medium': 200,
                                        'large': 250,
                                        'full': 'full' 
                                      },
                                  'inline_media.pictureset':
                                      { 
                                        'mini': (80, 80),
                                        'small': (150, 150),
                                        'medium': (200, 200),
                                        'large': (250, 250),
                                        'full': (380, 280) 
                                      } 
                                }


.. index::
   single: INLINE_MEDIA_DEFAULT_SIZE
   pair: Setting; INLINE_MEDIA_DEFAULT_SIZE

``INLINE_MEDIA_DEFAULT_SIZE``
=============================

**Optional**

This setting establishes the default size in case an entry corresponding to an ``app_label.model`` and ``class`` doesn't exist in ``INLINE_MEDIA_CUSTOM_SIZES``.

It defaults to::

    INLINE_MEDIA_DEFAULT_SIZE = 200


.. index::
   single: INLINE_MEDIA_DEFAULT_SIZE
   pair: Setting; INLINE_MEDIA_DEFAULT_SIZE

``INLINE_MEDIA_TEXTAREA_ATTRS``
===============================

**Optional**

This setting define attributes to apply to ``TextareaWithInlines`` widgets. 

To apply common attributes to all ``TextareaWithInline`` widgets use the **default** key, and define attributes and values in its dictionary (see the example below).

You can also apply rendering attributes on a per ``app_label.model`` and ``field`` basis. 

In the following example, fields of type ``TextFieldWithInlines`` get the ``style`` attribute applied by default. Then the ``abstract`` and ``body`` fields of the ``articles.article`` model get the attribute ``rows`` applied too. The ``style`` attribute defined in the **default** key can be overriden by simply defining it again for an ``app_label.model/field`` combination::

    INLINE_MEDIA_TEXTAREA_ATTRS = {
                                      'default': {
                                          'style': 'font: 13px monospace',
                                      },    
                                      'articles.article': {
                                          'abstract': { 'rows':  5 },
                                          'body':     { 'rows': 20 }
                                      }    
                                  }

Defaults to ``{}`` so that no extra attributes are applied.


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
