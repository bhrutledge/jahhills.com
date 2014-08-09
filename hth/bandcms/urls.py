from django.conf.urls import patterns, include, url
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Gig, Release, Song, Video
from . import views

# TODO: release_patterns = patterns('', list_url(Release), detail_url(Release))
# TODO: Move logic into views.py
# TODO: Use namespaces

post_patterns = patterns('',
    url(r'^$',
        views.PostListView.as_view(),
        name='post_list'),
    url(r'^(?P<slug>[-_\w]+)/$',
        views.PostDetailView.as_view(),
        name='post_detail'),
)

gig_patterns = patterns('',
    url(r'^$',
        ListView.as_view(queryset=Gig.published.all()), name='gig_list'),
)

release_patterns = patterns('',
    url(r'^$',
        ListView.as_view(queryset=Release.published.all()),
        name='release_list'),
    url(r'^(?P<slug>[-_\w]+)/$',
        DetailView.as_view(queryset=Release.published.all()),
        name='release_detail'),
)

song_patterns = patterns('',
    url(r'^$',
        ListView.as_view(queryset=Song.published.all()),
        name='song_list'),
    url(r'^(?P<slug>[-_\w]+)/$',
        DetailView.as_view(queryset=Song.published.all()),
        name='song_detail'),
)

video_patterns = patterns('',
    url(r'^$',
        ListView.as_view(queryset=Video.published.all()),
        name='video_list'),
    url(r'^(?P<slug>[-_\w]+)/$',
        DetailView.as_view(queryset=Video.published.all()),
        name='video_detail'),
)

urlpatterns = patterns('',
    url(r'^posts/', include(post_patterns)),
    url(r'^gigs/', include(gig_patterns)),
    url(r'^releases/', include(release_patterns)),
    url(r'^songs/', include(song_patterns)),
    url(r'^videos/', include(video_patterns)),
)

