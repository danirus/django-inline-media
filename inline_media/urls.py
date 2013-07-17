#-*- coding: utf-8 -*-

from django import VERSION as DJANGO_VERSION
if DJANGO_VERSION[0:2] < (1, 4):
    from django.conf.urls.defaults import patterns, url
else:
    from django.conf.urls import patterns, url

from django.contrib.auth.decorators import login_required
from inline_media.views import render_inline

urlpatterns = patterns('',
    url('^render-image/(?P<size>[\d]+)/(?P<align>[\w]+)/(?P<oid>[\d]+)$', 
        login_required(render_inline, redirect_field_name=""),
        name="inline-media-render-inline"),
)
