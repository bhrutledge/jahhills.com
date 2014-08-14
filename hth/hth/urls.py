from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='hth/home_page.html')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^news/', include('news.urls')),
    url(r'^shows/', include('shows.urls')),
    url(r'^music/', include('music.urls')),
#    url(r'^videos/', include(bandcms.urls.video_patterns)),
)

