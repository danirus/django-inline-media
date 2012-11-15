.. _ref-tutorial:

========
Tutorial
========

Django-inline-media is a simple reusable app that allows insertion of inline media content into TextFields. 


.. index::
   single: Motivation

Motivation
==========

You might find this application useful if you need to add inline content to a TextField. A blogging app is a good candidate. In general, any custom model in your project aimed to show text combined with inline media may benefit from it. 

Django-inline-media comes with two media models: Picture and PictureSet, but you can create yours to support other media formats or providers.

This tutorial explains how to install and configure django-inline-media, how to integrate it in your web project and how to use the new widget.

It additionally supports the Wysihtml5 rich text editor by providing a replacement for the Wysihtml5's ``insertImage`` command. See the **demo_wysihtml5** for details on this feature.


.. index::
   single: Installation

Installation
============

Installing Django-inline-media is as simple as checking out the source and adding it to your project or ``PYTHONPATH``.

Use git, pip or easy_install to check out Django-inline-media from Github_ or get a release from PyPI_:

  1. Use **git** to clone the repository, and then install the package (read more about git_):

    * ``git clone git://github.com/danirus/django-inline-media.git`` and

    * ``python setup.py install``

  2. Or use **pip** (read more about pip_):

    * Do ``pip install django-inline-media``, or

    * Edit your project's ``requirements`` file and append either the Github_ URL or the package name ``django-inline-media``, and then do ``pip install -r requirements``.

  3. Or use **easy_install** (read more about easy_install_): 

    * Do ``easy_install django-inline-media``


.. _Github: http://github.com/danirus/django-inline-media
.. _PyPI: http://pypi.python.org/
.. _pip: http://www.pip-installer.org/
.. _easy_install: http://packages.python.org/distribute/easy_install.html
.. _git: http://git-scm.com/


.. index::
   single: Configuration

Configuration
=============

Configuration comprehends the following steps:

1. Install required apps:

  * ``sorl.thumbnail``: http://pypi.python.org/pypi/sorl-thumbnail/
  * ``tagging``: http://pypi.python.org/pypi/tagging/

2. Add the following entries in your ``settings.py``:

 * Add ``inline_media``, ``sorl.thumbnail`` and ``tagging`` to ``INSTALLED_APPS``.
 * Add ``THUMBNAIL_BACKEND = "inline_media.sorl_backends.AutoFormatBackend"``
 * Add ``THUMBNAIL_FORMAT = "JPEG"``
 * Optionally you can add an extra setting to control where django-inline-media stores images (see :doc:`settings`), but it has a sane default.

3. Run the following django manage commands:

   * ``python manage.py syncdb`` to create the inline_media DB entities (InlineType, License, Picture, PictureSet)
   * ``python manage.py collectstatic`` to copy CSS and Javascript content from inline_media into your project's static directory


There are a few extra details to consider when planning to use the Wysihtml5 editor. Read on the specific :ref:`ref-wysihtml5-demo`.


.. index::
   single: inline-media

.. _using-label:

Using inline-media
==================

Using inline-media is pretty straightforward:

1. Decide which fields of your models will hold inline media content (the typical candidate: a ``body`` field of a blog ``Post`` model)

2. Change their type from **TextField** to **TextFieldWithInlines**. This change does not affect your models' table definition, it does affect the way the field is rendered
 
3. Change the admin class of those models and make them inherit from **AdminTextFieldWithInlinesMixin**. This change make fields of type **TextfieldWithInlines** be rendered as **TextareWithInlines**

Let's see it with an example: the Article model.


.. index::
   single: Code
   Pair: Example; Code

Example code
------------

The Article model, in the demo project, has a couple of fields of type TextField, ``abstract`` and ``body``. Only the field ``body`` may have inline media content. Django-inline-media comes with a new field **TextFieldWithInlines** that extends Django's **TextField** to support inline media content insertion. The new Article's definition will use the new type for the ``body`` field::

    from inline_media.fields import TextFieldWithInlines

    class Article(models.Model):
        title = models.CharField(max_length=200)
	slug = models.SlugField(unique_for_date='publish')
	abstract = models.TextField()
	body = TextFieldWithInlines()
	publish = models.DateTimeField(default=datetime.now)


And the ArticleAdmin class will inherit from both, **AdminTextFieldWithInlinesMixin** and Django's **ModelAdmin**::

    from django.contrib import admin
    from inline_media.admin import AdminTextFieldWithInlinesMixin
    from demo.articles.models import Article

    class ArticleAdmin(AdminTextFieldWithInlinesMixin, admin.ModelAdmin):
	list_display  = ('title', 'publish')
	list_filter   = ('publish',)
	search_fields = ('title', 'abstract', 'body')
	prepopulated_fields = {'slug': ('title',)}
	fieldsets = ((None, 
		      {'fields': ('title', 'slug', 'abstract', 'body', 
				  'publish',)}),)

    admin.site.register(Article, ArticleAdmin)


.. index::
   single: InlineType

InlineType instances
====================

Four models are available when installing inline_media:

1. **InlineType**: Media models are registered as InlineType instances
2. **License**: Licenses under which media content is publicly available or distributed
3. **Picture**: Pictures with title, description, tags, author, license...
4. **PictureSet**: Collections of pictures

In order to insert inline content in your text fields you have to:

1. Create a new media model (Picture, PictureSet, Video, VideoSet...).
2. Create a new InlineType instance and use the model of the previous point as the content type for the instance.
3. Optionally create a new template to render the media content provided by the model.
4. Go to your Admin site, write your text fields and insert new media content using the new InlineType.

Look at the demo project admin site. See that **Picture** and **PictureSet** are already instances of **InlineType**. Then click on any of the articles admin change view and see that the **inlines** field below the **body** allows you to choose between inline types Picture and PictureSet:

.. image:: images/tutorial_article_change_view.png

Later when rendering articles detail (``example/demo/templates/articles/article_detail.html``) you have to load the ``inlines`` templatetag and apply the ``render_inlines`` filter to the ``body`` field::

    {% load i18n inlines %}
    ...

    <div class="inline_media_clearfix">
      {{ object.body|render_inlines }}
    </div>

And the filter will use the template ``inline_media/templates/inline_media/inline_media_pictureset.html`` to render the inline media.

