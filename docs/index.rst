.. django-inline-media documentation master file, created by
   sphinx-quickstart on Mon Dec 19 19:20:12 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Introduction
============

**django-inline-media** allows insertion of inline media content in your text fields. Based on `django-basic-apps/inlines <https://github.com/nathanborror/django-basic-apps>`_, it provives the following features:

.. index::
   single: Features

1. Inserts pictures and collection of pictures into your texts using the ``TextAreaWithInlines`` widget.
2. Positions media content at different places and sizes (mini/small/medium/large at left/right or full at the left/center/right).
3. Facilitates administration with thumbnails and search by tags, author and license.
4. Shows a customised control to insert media content in text fields.
5. Uses jquery `prettyPhoto <http://www.no-margin-for-errors.com/projects/prettyphoto-jquery-lightbox-clone/>`_ to show pictures and galleries when clicking on them.
6. Replaces django-wysihtml5 ``insertImage`` command with a custom ``insertInlinePicture``.


The following sample shows a centered inline picture set inserted in a text, on mouseover event the first 3 photos unfold:

.. image:: images/cover.png

Run the demo project to see django-inline-media in action.

.. toctree::
   :maxdepth: 2

   example
   tutorial
   templatetags
   settings
   templates


.. index::
   pair: Quick; Start

Quick start
===========

1. Get the dependencies:

 * `Django Sorl-Thumbnail <http://thumbnail.sorl.net/>`_
 * `Django Tagging <http://code.google.com/p/django-tagging/>`_

2. In your ``settings.py``:

 * Add ``inline_media``, ``sorl.thumbnail`` and ``tagging`` to ``INSTALLED_APPS``.

 * Add ``THUMBNAIL_BACKEND = "inline_media.sorl_backends.AutoFormatBackend"``

 * Add ``THUMBNAIL_FORMAT = "JPEG"``

3. Create a model with a field of type ``TextFieldWithInlines``.

4. Create an admin class for that model by inheriting from both ``inline_media.admin.AdminTextFieldWithInlinesMixin`` and Django's ``admin.ModelAdmin``.

5. Optionally, customise inline_media templates by copying them from ``inline_media/templates/inline_media/`` to your ``inline_media/`` folder in your templates directory.

5. Run ``manage.py`` commands: ``syncdb``, ``collectstatic``, ``runserver``.

6. Create two `InlineType` objects, one for the `Picture` model and one for the `PictureSet` model.

7. Upload some pictures and create some picture sets.

8. Add content to the model using the field ``TextFieldWithInlines`` and see that you can insert inline content in the textarea. It will be rendered in the position indicated by the CSS class selected in the dropdown box.

9. Hit your app's URL!

Run the **demo** in ``django-inline-media/examples/demo`` to see an example.


If you prefer to use Wysihtml5 for your textareas (beta):

1. Get the widget from `Django Wysihtml5 <http://github.com/danirus/django-wysihtml5>`_.

2. In your ``settings.py``:

 * Add ``wysihtml5 to ``INSTALLED_APPS``.

 * Add ``WYSIHTML5_CMD_INSERT_IMAGE = "insertInlinePicture"``

 * Add ``WYSIHTML5_FUNC_INSERT_IMAGE_DIALOG = "inline_media.widgets.render_insert_inline_picture_dialog"``

3. Add ``url(r'^inline-media/', include('inline_media.urls'))`` to your urls module.

4. Create a model with a field of type ``Wysihtml5TextField``.

5. Create an admin class for that model by inheriting from both ``inline_media.admin.AdminWysihtml5TextFieldMixin`` and Django's ``admin.ModelAdmin``.

6. Hit your app's URL!

Run the **wysihtml5_demo** in ``django-inline-media/examples/demo_wysihtml5`` to see an example.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

