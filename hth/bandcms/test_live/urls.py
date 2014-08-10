from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

import bandcms.urls

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(bandcms.urls)),
)

