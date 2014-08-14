from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns('',
    url(r'^songs/$',
        views.SongListView.as_view(),
        name='song_list'),
    url(r'^songs/(?P<slug>[-_\w]+)/$',
        views.SongDetailView.as_view(),
        name='song_detail'),
    url(r'^$',
        views.ReleaseListView.as_view(),
        name='release_list'),
    url(r'^(?P<slug>[-_\w]+)/$',
        views.ReleaseDetailView.as_view(),
        name='release_detail'),
)

