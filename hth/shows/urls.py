from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$',
        views.GigListView.as_view(),
        name='gig_list')
]
