from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve

from demo import views

admin.autodiscover()


urlpatterns = [
    url(r'^admin/',    include(admin.site.urls)),
    url(r'^articles/', include('demo.articles.urls')),
    url(r'^$',         views.homepage_v, name='homepage'),
]


if settings.DEBUG:
    # urlpatterns += staticfiles_urlpatterns()
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
