from django.conf.urls import url
from django.views.generic import ListView, DateDetailView

from demo.articles.models import Article


urlpatterns = [
    url(r'^$', 
        ListView.as_view(queryset=Article.objects.published()),
        name='articles-index'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/'
        r'(?P<slug>[-\w]+)/$',
        DateDetailView.as_view(model=Article, date_field="publish", 
                               month_format="%m"), 
        name='articles-article-detail'),
]
