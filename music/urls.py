from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^music/$',
        views.ReleaseListView.as_view(),
        name='release_list'),
    url(r'^music/(?P<slug>[-_\w]+)/$',
        views.ReleaseDetailView.as_view(),
        name='release_detail'),
    url(r'^music/(?P<slug>[-_\w]+)/lyrics/$',
        views.ReleaseLyricsView.as_view(),
        name='release_lyrics'),
    url(r'^songs/$',
        views.SongListView.as_view(),
        name='song_list'),
    url(r'^songs/(?P<slug>[-_\w]+)/$',
        views.SongDetailView.as_view(),
        name='song_detail'),
    url(r'^video/$',
        views.VideoListView.as_view(),
        name='video_list'),
    url(r'^video/(?P<slug>[-_\w]+)/$',
        views.VideoDetailView.as_view(),
        name='video_detail'),
    url(r'^press/$',
        views.PressListView.as_view(),
        name='press_list'),
]
