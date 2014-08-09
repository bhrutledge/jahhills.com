from django.conf.urls import patterns, include, url
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from . import views

# TODO: post_patterns = patterns('', list_url(Release), detail_url(Release))
# TODO: Use namespaces?

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
        views.GigListView.as_view(),
        name='gig_list')
)

release_patterns = patterns('',
    url(r'^$',
        views.ReleaseListView.as_view(),
        name='release_list'),
    url(r'^(?P<slug>[-_\w]+)/$',
        views.ReleaseDetailView.as_view(),
        name='release_detail'),
)

song_patterns = patterns('',
    url(r'^$',
        views.SongListView.as_view(),
        name='song_list'),
    url(r'^(?P<slug>[-_\w]+)/$',
        views.SongDetailView.as_view(),
        name='song_detail'),
)

video_patterns = patterns('',
    url(r'^$',
        views.VideoListView.as_view(),
        name='video_list'),
    url(r'^(?P<slug>[-_\w]+)/$',
        views.VideoDetailView.as_view(),
        name='video_detail'),
)

urlpatterns = patterns('',
    url(r'^posts/', include(post_patterns)),
    url(r'^gigs/', include(gig_patterns)),
    url(r'^releases/', include(release_patterns)),
    url(r'^songs/', include(song_patterns)),
    url(r'^videos/', include(video_patterns)),
)

