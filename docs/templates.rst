.. _ref-templates:

.. index::
   single: Templates

=========
Templates
=========

List of template files coming with Django-inline-media.

**inline_media/inline_media.picture.mini.html**
    Renders an ``<inline>`` picture with any of the followin CSS classes:
     * ``inline_mini_left`` or ``inlin_mini_right``.

**inline_media/inline_media.picture.default.html**
    Renders an ``<inline>`` picture with any of the following CSS classes:
     * ``inline_small_left`` or ``inlin_small_right``
     * ``inline_medium_left`` or ``inlin_medium_right``
     * ``inline_large_left`` or ``inlin_large_right``

**inline_media/inline_media.picture.full.html**
    Renders an ``<inline>`` picture with any of the following CSS classes:
    * ``inline_full_left``, ``inline_full_center``, ``inlin_full_right``.

**inline_media/inline_media.pictureset.mini.html**
    Renders an ``<inline>`` pictureset with any of the followin CSS classes:
     * ``inline_mini_left`` or ``inline_mini_right``.

**inline_media/inline_media.pictureset.default.html**
    Renders an ``<inline>`` pictureset with any of the following CSS classes:
     * ``inline_small_left`` or ``inline_small_right``
     * ``inline_medium_left`` or ``inline_medium_right``
     * ``inline_large_left`` or ``inline_large_right``

**inline_media/inline_media.pictureset.full.html**
    Renders an ``<inline>`` pictureset with any of the followin CSS classes:
     * ``inline_full_left``, ``inline_full_center``, ``inline_full_right``.


.. index::
   single: customization
   pair: template; customization
   triple: INLINE_MEDIA_CUSTOM_SIZES; template; customization
   

Template customization
----------------------

Django-inline-media will try to use a template matching the following pattern:

* ``inline_media/<app-label>.<model>.<size>.html``
  Being ``<size>`` one of the following:

  * mini
  * small
  * medium
  * large
  * full

  **Note**: Actual size values can be customize through the setting ``INLINE_MEDIA_CUSTOM_SIZES``. See it the :doc:`settings`.

When django-inline-media has to render an element with a CSS class like ``inline_medium_left``, it will first look for the template:

* ``inline_media/<app_label>.<model>.medium.html``

And if it doesn't exist it will use the default template:

* ``inline_media/<app_label>.<model>.default.html``


Your own InlineTypes
--------------------

If the django-inline-media models, Picture and PictureSet, are not suitable for your project or need another ones, just create your own and bind them to the app. 

Once you have your model (say ``MyPicture``), declare it the setting ``INLINE_MEDIA_TYPES``. Your model will then show up in the dropdown list of inline types at the bottom of your ``TextFieldWithInlines`` fields (like the ``body`` field in the Article model of the demo).

Then create templates to render your own media content. Name your templates after the correspoding ``app_label`` for your model:

  * ``inline_media/<my_app_label>.mypicture.<size>.html``
  * ``inline_media/<my_app_label>.mypicture.default.html``
