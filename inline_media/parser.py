# code borrowed from django-basic-apps by Nathan Borror
# https://github.com/nathanborror/django-basic-apps

from django.template import TemplateSyntaxError
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.utils.encoding import smart_unicode
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

try:
    from BeautifulSoup import BeautifulStoneSoup
except ImportError:
    from beautifulsoup import BeautifulStoneSoup


class MySoup(BeautifulStoneSoup):
    def __init__(self, *args, **kwargs):
        self.PRESERVE_WHITESPACE_TAGS.append("pre")
        BeautifulStoneSoup.__init__(self, *args, **kwargs)


def inlines(value, return_list=False):
    selfClosingTags = ['inline','img','br','input','meta','link','hr']
    soup = MySoup(value, selfClosingTags=selfClosingTags)
    inline_list = []
    if return_list:
        for inline in soup.findAll('inline'):
            rendered_inline = render_inline(inline)
            inline_list.append(rendered_inline['context'])
        return inline_list
    else:
        for inline in soup.findAll('inline'):
            rendered_inline = render_inline(inline)
            inline.replaceWith(render_to_string(rendered_inline['template'], rendered_inline['context']))
        html_content = "".join(["%s" % element for element in soup.contents])
        return mark_safe(html_content)


def render_inline(inline):
    """
    Replace inline markup with template markup that matches the
    appropriate app and model.

    """

    # Look for inline type, 'app.model'
    try:
        app_label, model_name = inline['type'].split('.')
    except:
        if settings.DEBUG:
            raise TemplateSyntaxError, "Couldn't find the attribute 'type' in the <inline> tag."
        else:
            return ''

    # Look for content type
    try:
        content_type = ContentType.objects.get(app_label=app_label, model=model_name)
        model = content_type.model_class()
    except ContentType.DoesNotExist:
        if settings.DEBUG:
            raise TemplateSyntaxError, "Inline ContentType not found."
        else:
            return ''

    # Check for an inline class attribute
    try:
        inline_class = smart_unicode(inline['class'])
    except:
        inline_class = ''

    try:
        try:
            id_list = [int(i) for i in inline['ids'].split(',')]
            obj_list = model.objects.in_bulk(id_list)
            obj_list = list(obj_list[int(i)] for i in id_list)
            context = { 'object_list': obj_list, 'class': inline_class }
        except ValueError:
            if settings.DEBUG:
                raise ValueError, "The <inline> ids attribute is missing or invalid."
            else:
                return ''
    except KeyError:
        try:
            obj = model.objects.get(pk=inline['id'])
            context = { 'content_type':"%s.%s" % (app_label, model_name), 'object': obj, 'class': inline_class, 'settings': settings }
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
        'template':"inline_media/%s_%s.html" % (app_label, model_name), 
        'context':context 
    }

    return rendered_inline
