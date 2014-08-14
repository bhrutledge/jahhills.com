from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^$',
        views.ReleaseListView.as_view(),
        name='release_list'),
    url(r'^(?P<slug>[-_\w]+)/$',
        views.ReleaseDetailView.as_view(),
        name='release_detail'),
)

