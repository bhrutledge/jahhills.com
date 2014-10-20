from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns('',  # noqa
    url(r'^music/$',
        views.ReleaseListView.as_view(),
        name='release_list'),
    url(r'^music/(?P<slug>[-_\w]+)/$',
        views.ReleaseDetailView.as_view(),
        name='release_detail'),
    url(r'^songs/$',
        views.SongListView.as_view(),
        name='song_list'),
    url(r'^songs/(?P<slug>[-_\w]+)/$',
        views.SongDetailView.as_view(),
        name='song_detail'),
    url(r'^videos/$',
        views.VideoListView.as_view(),
        name='video_list'),
    url(r'^videos/(?P<slug>[-_\w]+)/$',
        views.VideoDetailView.as_view(),
        name='video_detail'),
)
