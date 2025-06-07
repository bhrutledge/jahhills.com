from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='home_page'),
    url(r'^about/$', views.AboutPageView.as_view(), name='about_page'),
    url(r'^news/', include('hth.news.urls')),
    url(r'^live/', include('hth.shows.urls')),
    url(r'^', include('hth.music.urls')),
]

if settings.MEDIA_URL and settings.MEDIA_ROOT:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

# TODO: Debug-only until HTTPS is configured
if settings.DEBUG:
    urlpatterns += [
        url(r'^admindocs/', include('django.contrib.admindocs.urls')),
        url(r'^admin/', include(admin.site.urls)),
    ]

urlpatterns += [
    url(r'^(?P<template_name>[a-zA-Z0-9-_]+)/$', views.NetlifyTemplateView.as_view()),
]
