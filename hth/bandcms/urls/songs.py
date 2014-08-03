from django.conf.urls import patterns, url
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from ..models import Song

urlpatterns = patterns('',
    url(r'^$',
        ListView.as_view(queryset=Song.published.all()),
        name='song_list'),
    url(r'^(?P<slug>[-_\w]+)/$',
        DetailView.as_view(queryset=Song.published.all()),
        name='song_detail'),
)


