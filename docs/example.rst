.. _ref-example:

============
Demo project
============

Django-inlines-media comes with a demo project to show the application in action.


Demo project setup
==================

1. Go to the demos directory ``django_inline_media/example/demo``.

2. Run ``python manage.py syncdb --noinput`` to create a simple SQLite db file for the demo (``user:admin``, ``pwd:admin``).

3. Run ``python manage.py collectstatic`` and answer *'Yes'*, to collect static files from ``inline_media/static/``.

4. Run ``python manage runserver`` and visit http://localhost:8000/ 


Demo project structure
======================

The home page shows a link to an article list. The article list contains six example articles. Each of which contains pictures or picture sets located at different positions in the text. Take a look at the articles and click on the media. Pictures and picture sets are clickable by default. When clicking on a picture, the prettyPhoto jquery plugin overlays the picture on the current page. When clicking on a picture set, the plugin overlays a gallery view of all the pictures in the picture set.

The demo site uses **django-inline-media** with a custom **articles** app. The **articles** app defines the **Article** model. **django-inlines-media** provides 4 models: **InlineType**, **License**, **Picture** and **PictureSet**:

.. image:: images/demo_admin.png

The **Article** model has a **body** field of type **TextFieldWithInlines**. The field uses its own widget **TextareaWithInlines** that renders an extra control to insert inline media in the textarea. The inline media content can be placed at different positions and with different size.

Position can either be **left**, **right**, or **centered**. The size can be **small** (150px width), **medium** (200px width) or **large** (250px width). Pictures positioned centred are shown at **full size**, and centred picture sets use a frame of 380x280 pixels.


Example articles
===================

Let's see how articles in the demo site look like. Following you can see example articles one, two and five. Article views are combined with their body fields in the admin UI so that you can get an idea of how inline elements look like in the textarea and what's the effect in the final rendered article.

Example article one
-------------------

Article one is made of four text paragraphs with a picture. The picture and its description float at the right hand side of the first paragraph.

.. image:: images/demo_article_1.png

The code highlighted in blue inserts the Ubuntu logo at the top right side of the article's text. It's been added using the control **Inlines** below the body's textarea.

The attribute *type* in the *<inline>* corresponds with the *InlineType* instance of the content_type *Picture*. The attribute *id* is the object id of the picture, and *class* represents the CSS class applied when rendering the inline with the template ``templates/inline_media/inline_media_picture.html``.


Example article two
-------------------

Yet another four paragraphs example article with two pictures, both floating at the right hand side, the first one on the first paragraph and the second on the second paragraph. 

.. image:: images/demo_article_2.png

The Python logo uses the CSS class *inline_large_right* while the Django logo uses *inline_medium_right*. Both are clickable and both contain a description with an anchor element. 

The change picture view for the first image, the Python one, looks like this:

.. image:: images/demo_pic_change_view_python.png

Removing the tick of the box *Show as link* avoids making the image clickable. As an alternative you can also rewrite the template ``inline_media/inline_media_picture.html`` using the attributes at will. Take a look at the Article 4 to see an example with an inline non-clickable picture.


Example article five
--------------------

Three paragraphs with an inline picture set. The picture set float at the right side using the *inline_medium_right* CSS class.

.. image:: images/demo_article_5.png

An inline picture set has different looks: 

 * **As an inline**: the picture set shows only the croped version of the cover picture. 
 * **On mouseover**: A croped version of the 2/3 first pictures of the set are fanned out.
 * **On click**: The picture set is overlaid in a gallery view showing complete pictures.

The overlaid gallery view of the picture set of article five:

.. image:: images/demo_article_5_gallery.png
