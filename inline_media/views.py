from __future__ import unicode_literals

try:
    import json
except ImportError:
    from django.utils import simplejson as json

from django.http import HttpResponse
from sorl.thumbnail import get_thumbnail
from inline_media.conf import settings
from inline_media.models import Picture


def render_inline(request, size, align, oid):
    try:
        picture = Picture.objects.get(pk=oid)
    except Picture.DoesNotExist:
        if settings.DEBUG:
            raise Picture.DoesNotExist("Picture id '%s' does not exist")
        else:
            return ''
    im = get_thumbnail(picture.picture, size)
    data = json.dumps({"src": im.url,
                       "title": picture.title,
                       "width": size,
                       "align": align})
    return HttpResponse(data, content_type='application/json')
