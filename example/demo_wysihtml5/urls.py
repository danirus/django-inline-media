from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


admin.autodiscover()

urlpatterns = patterns('demo_wysihtml5.views',
    url(r'^inline-media/', include('inline_media.urls')),
    url(r'^admin/',    include(admin.site.urls)),
    url(r'^articles/', include('demo_wysihtml5.articles.urls')),
    url(r'^$',         'homepage_v', name='homepage'),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns(
        "",
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                'document_root': settings.MEDIA_ROOT,
        }),
    )
