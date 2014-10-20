from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns('',  # noqa
    url(r'^$',
        views.GigListView.as_view(),
        name='gig_list')
)
