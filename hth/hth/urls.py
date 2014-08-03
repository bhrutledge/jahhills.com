from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='hth/home_page.html')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^news/', include('bandcms.urls.posts')),
    url(r'^calendar/', include('bandcms.urls.gigs')),
    url(r'^music/songs/', include('bandcms.urls.songs')),
    url(r'^music/', include('bandcms.urls.releases')),
)

