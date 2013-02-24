.. _ref-templatetags:

.. index::
   single: Filters

=======
Filters
=======

Django-inline-media comes with two filters and one tag:

 * filter ``render_inlines``
 * filter ``extract_inlines``

Load the templatetag module to use them in your templates::

    {% load inlines %}


.. index::
   single: render_inlines
   pair: Filter; render_inlines

Filter: render_inlines
======================

Renders inlines in a text by passing them through inline templates. 

Syntax::

    {{ <field>|render_inlines }}

Inline Syntax (singular)::

    <inline type="<app_name>.<model_name>" id="<id>" class="<cssclass>" />

Inline Syntax (plural)::

    <inline type="<app_name>.<model_name>" ids="<id>, <id>, <id>" />

An inline template will be used to render the inline. Templates will be located in the following maner:
    ``inline_media/<app_name>_<model_name>.html``

The template will be passed the following context:
  * **object**: an object for the corresponding passed id,  or
  * **object_list**: a list of objects for the corresponding ids.

It would be wise to anticipate both object_list and object unless you know for sure one or the other will only be present.

Example usage::

    {{ object.body|render_inlines }}


.. index::
   single: extract_inlines
   pair: Filter; extract_inlines

Filter: extract_inlines
=======================

Extract inlines from a text.

Syntax::

    {{ <field>|extract_inlines }}

Example usage::

    {% for inline in object.body|extract_inlines %}
      {% ifequal inline.content_type "inline_media.picture" %}
        {% include "inline_media/inline_media_picture.html" with object=inline.object class=inline.class %}
      {% endifequal %}
    {% endfor %}
