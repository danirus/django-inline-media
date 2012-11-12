#-*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.template import TemplateSyntaxError
from django.shortcuts import render_to_response


def render_inline(request, app_label, model_name, css_class, oid):
    try:
        content_type = ContentType.objects.get(app_label=app_label, model=model_name)
        model = content_type.model_class()
    except ContentType.DoesNotExist:
        if settings.DEBUG:
            raise TemplateSyntaxError, "Inline ContentType not found."
        else:
            return ''

    context = { 'content_type': '%s.%s' % (app_label, model_name), 
                'class': css_class, 
                'settings': settings }
    try:
        obj = model.objects.get(pk=oid)
        context['object'] = obj
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
            
    return render_to_response("inline_media/%s_%s.html" % (app_label, model_name),
                            context)
