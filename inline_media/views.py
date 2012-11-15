#-*- coding: utf-8 -*-

from django.http import HttpResponse
from django.template import TemplateSyntaxError
from django.shortcuts import render_to_response
from django.utils import simplejson

from sorl.thumbnail import get_thumbnail

from inline_media.models import Picture


def render_inline(request, size, align, oid):
    import ipdb; ipdb.set_trace()
    try:
        picture = Picture.objects.get(pk=oid)
    except Picture.DoesNotExist:
        if settings.DEBUG:
            raise Picture.DoesNotExist, "Picture id '%s' does not exist"
        else:
            return ''
    im = get_thumbnail(picture.picture, size)
    json = simplejson.dumps({"src": im.url, 
                             "title": picture.title, 
                             "width": size, 
                             "align": align})
    return HttpResponse(json, mimetype='application/json')
