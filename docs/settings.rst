.. _ref-settings:


.. index::
   single: Settings

========
Settings
========

Django-inline-media recognizes four setting:


.. index::
   single: INLINE_MEDIA_TYPES
   pair: Setting; INLINE_MEDIA_TYPES

``INLINE_MEDIA_TYPES``
======================

**Optional**

Defines the inline media types available project wide. 

It defaults to::

    INLINE_MEDIA_TYPES = ['inline_media.picture',
                          'inline_media.pictureset']


.. index::
   single: INLINE_MEDIA_CUSTOM_SIZES
   pair: Setting; INLINE_MEDIA_CUSTOM_SIZES

``INLINE_MEDIA_CUSTOM_SIZES``
=============================

**Optional**

This setting defines custom size values for the available ``INLINE_MEDIA_TYPES``. By default every inline type declared in ``INLINE_MEDIA_TYPES`` can be rendered in **mini**, **small**, **medium**, **large** and **full** size.

``INLINE_MEDIA_CUSTOM_SIZES`` is a 2-level depth dictionary to define custom size values for each of the 5 size classes. Size classes can also be disabled. 

The first level contains inline types with **app_label.model** pairs as keys.  The second level contains class sizes as keys and values as geometries. When the value is just an **int**, it represents the **width** of the thumbnail. When the value is a **tuple** it represents the **(width, height)** of the thumbnail. The value can be ``None``, what means the size won't be available for that inline type.

It defaults to::

    INLINE_MEDIA_CUSTOM_SIZES = { 
        'inline_media.picture': { 
            'mini': 80,
            'small': 150,
            'medium': 200,
            'large': 250,
        },
        'inline_media.pictureset': { 
            'mini': None,
            'small': (150, 150),
            'medium': (200, 200),
            'large': (250, 250),
            'full': (380, 280) 
        } 
    }

See that the 'full' class size is not defined for the type ``inline_media.picture``. That doesn't disable it. By default the 5 class sizes are active for every inline type defined in ``INLINE_MEDIA_TYPES``. The purpose of this setting is either to pass a custom size in the context to the template, or to disable a class size. 

To disable the 'small' size for type ``inline_media.pictureset`` just set it to ``None`` in your settings module::

    INLINE_MEDIA_CUSTOM_SIZES = {
        'inline_media.pictureset': {
            'small': None,
        }
    }

.. index::
   single: INLINE_MEDIA_TEXTAREA_ATTRS
   pair: Setting; INLINE_MEDIA_TEXTAREA_ATTRS

``INLINE_MEDIA_TEXTAREA_ATTRS``
===============================

**Optional**

This setting define attributes to apply to ``TextareaWithInlines`` widgets. 

To apply common attributes to all ``TextareaWithInline`` widgets use the **default** key, and define attributes and values in its dictionary (see the example below).

You can also apply rendering attributes on a per ``app_label.model`` and ``field`` basis. 

In this example, every ``TextFieldWithInlines`` field will get the ``style`` attribute applied by default. Then, ``abstract`` and ``body`` fields of the ``articles.article`` model will get the attribute ``rows`` applied too. The ``style`` attribute defined in the **default** key can be overriden by simply defining it again for an ``app_label.model/field`` combination::

    INLINE_MEDIA_TEXTAREA_ATTRS = {
        'default': {
            'style': 'font: 13px monospace',
        },    
        'articles.article': {
            'abstract': { 
                'rows':  5 
            },
            'body': { 
                'rows': 20 
            }
        }    
    }

Defaults to ``{}`` so that no extra attributes are applied.


.. index::
   single: INLINE_MEDIA_REMOVE_TAGS
   pair: Setting; INLINE_MEDIA_REMOVE_TAGS

``INLINE_MEDIA_REMOVE_TAGS``
============================

**Optional**

This setting list all the tags that could be added by the parser 'html.parser' used with BeautifulSoup4 to render the content of TextFieldWithInlines. 'html.parser' is the only parser available under Python 3 at the moment.

An example::

    INLINE_MEDIA_REMOVE_TAGS = ['</br>', </whatever>']

Defaults to ``['</br>']``


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
