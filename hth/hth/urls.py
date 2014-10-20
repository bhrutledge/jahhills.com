from django.conf.urls import patterns, include, url
from django.contrib import admin

from . import views


urlpatterns = patterns('',  # noqa
    url(r'^$', views.HomePageView.as_view(), name='home_page'),
    url(r'^admindocs/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^news/', include('news.urls')),
    url(r'^shows/', include('shows.urls')),
    url(r'^', include('music.urls')),
)
