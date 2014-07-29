from django.conf.urls import patterns, url
from django.views.generic.list import ListView

from ..models import Gig

urlpatterns = patterns('',
    url(r'^$',
        ListView.as_view(queryset=Gig.published.all()), name='gig_list'),
)

