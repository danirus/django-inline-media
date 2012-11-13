#-*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required

from inline_media.views import render_inline

urlpatterns = patterns('',
    url('^render-image/(?P<size>[\w\d]+)/(?P<align>[\w]+)/(?P<oid>[\d]+)$', 
        login_required(render_inline, redirect_field_name=""),
        name="inline-media-render-inline"),
)
