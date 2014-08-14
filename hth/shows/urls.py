from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns('',
    url(r'^$',
        views.GigListView.as_view(),
        name='gig_list')
)

