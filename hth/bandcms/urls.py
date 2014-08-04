from django.conf.urls import patterns, include, url
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Post, Gig, Release, Song


post_patterns = patterns('',
    url(r'^$',
        ListView.as_view(queryset=Post.published.all()), name='post_list'),
    url(r'^(?P<slug>[-_\w]+)/$',
        DetailView.as_view(queryset=Post.published.all()), name='post_detail'),
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

urlpatterns = patterns('',
    url(r'^posts/', include(post_patterns)),
    url(r'^gigs/', include(gig_patterns)),
    url(r'^releases/', include(release_patterns)),
    url(r'^songs/', include(song_patterns)),
)

