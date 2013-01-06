# code borrowed from django-basic-apps by Nathan Borror
# https://github.com/nathanborror/django-basic-apps

import re

from django.template import TemplateSyntaxError
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.utils.encoding import smart_unicode
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

try:
    from BeautifulSoup import BeautifulSoup, NavigableString
except ImportError:
    from beautifulsoup import BeautifulSoup, NavigableString

from inline_media.conf import DEFAULT_SIZE, CUSTOM_SIZES


def inlines(value, return_list=False):
    selfClosingTags = ['inline','img','br','input','meta','link','hr',]
    soup = BeautifulSoup(value, selfClosingTags=selfClosingTags)
    inline_list = []
    if return_list:
        for inline in soup.findAll('inline'):
            rendered_inline = render_inline(inline)
            inline_list.append(rendered_inline['context'])
        return inline_list
    else:
        for inline in soup.findAll('inline'):
            rendered_inline = render_inline(inline)
            rendered_item = BeautifulSoup(
                render_to_string(rendered_inline['template'], 
                                 rendered_inline['context']),
                selfClosingTags=selfClosingTags)
            inline.replaceWith(rendered_item)
        return mark_safe(soup)


regexp = re.compile(r'^inline_(?P<size_type>\w+)_\w+$')

def render_inline(inline):
    """
    Replace inline markup with template markup that matches the
    appropriate app and model.

    """

    # Look for the type attribute with 'app.model'
    try:
        inline_type = inline['type']
        app_label, model_name = inline_type.split('.')
    except:
        if settings.DEBUG:
            raise TemplateSyntaxError, "Couldn't find the attribute 'type' in the <inline> tag."
        else:
            return ''

    # Get the content type
    try:
        content_type = ContentType.objects.get(app_label=app_label, model=model_name)
        model = content_type.model_class()
    except ContentType.DoesNotExist:
        if settings.DEBUG:
            raise TemplateSyntaxError, "Inline ContentType not found."
        else:
            return ''

    # Look for the CSS class attribute
    try:
        inline_class = smart_unicode(inline['class'])
    except:
        if settings.DEBUG:
            raise TemplateSyntaxError, "Couldn't find the attribute 'class' in the <inline> tag."
        else:
            return ''

    # Get the size associated with the inline_class
    try:
        match = regexp.match(inline_class)
        if match:
            size_type = match.group('size_type')
        size = CUSTOM_SIZES[inline_type][size_type]
    except:
        size = DEFAULT_SIZE

    if type(size) == int:
        size = '%d' % size
    elif type(size) == tuple:
        size = '%dx%d' % size

    try:
        try:
            id_list = [int(i) for i in inline['ids'].split(',')]
            obj_list = model.objects.in_bulk(id_list)
            obj_list = list(obj_list[int(i)] for i in id_list)
            context = { 'object_list': obj_list, 
                        'class': inline_class,
                        'size': size }
        except ValueError:
            if settings.DEBUG:
                raise ValueError, "The <inline> ids attribute is missing or invalid."
            else:
                return ''
    except KeyError:
        try:
            obj = model.objects.get(pk=inline['id'])
            context = { 'content_type':"%s.%s" % (app_label, model_name), 
                        'object':obj, 
                        'class': inline_class,
                        'size': size }
        except model.DoesNotExist:
            if settings.DEBUG:
                raise model.DoesNotExist, "Object matching '%s' does not exist"
            else:
                return ''
        except:
            if settings.DEBUG:
                raise TemplateSyntaxError, "The <inline> id attribute is missing or invalid."
            else:
                return ''

    rendered_inline = {
        'template': [
            "inline_media/%s.%s.%s.html" % (app_label, model_name, size_type), 
            "inline_media/%s.%s.default.html" % (app_label, model_name) ],
        'context': context}
    return rendered_inline
