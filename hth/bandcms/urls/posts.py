from django.conf.urls import patterns, url
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from ..models import Post

urlpatterns = patterns('',
    url(r'^$',
        ListView.as_view(queryset=Post.published.all()), name='post_list'),
    url(r'^(?P<slug>[-_\w]+)/$',
        DetailView.as_view(queryset=Post.published.all()), name='post_detail'),
)

