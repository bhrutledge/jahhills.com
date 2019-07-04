from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

from . import views


urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='home_page'),
    url(r'^about/$', views.AboutPageView.as_view(), name='about_page'),
    url(r'^news/', include('hth.news.urls')),
    url(r'^live/', include('hth.shows.urls')),
    url(r'^', include('hth.music.urls')),

    url(r'^calendar',
        RedirectView.as_view(pattern_name='gig_list', permanent=True)),
    url(r'^music/releases/(?P<path>.*)',
        RedirectView.as_view(url='/music/%(path)s', permanent=True)),
    url(r'^music/songs/(?P<path>.*)',
        RedirectView.as_view(url='/songs/%(path)s', permanent=True)),
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
