from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from inline_media.views import render_inline


urlpatterns = [
    url('^render-image/(?P<size>[\d]+)/(?P<align>[\w]+)/(?P<oid>[\d]+)$',
        login_required(render_inline, redirect_field_name=""),
        name="inline-media-render-inline"),
]
