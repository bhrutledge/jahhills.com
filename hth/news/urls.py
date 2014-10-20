from django.conf.urls import patterns, url

from . import views

# TODO: post_patterns = patterns('', list_url(Post), detail_url(Post))
# TODO: Use namespaces?

urlpatterns = patterns('',  # noqa
    url(r'^$',
        views.PostListView.as_view(),
        name='post_list'),
    url(r'^(?P<slug>[-_\w]+)/$',
        views.PostDetailView.as_view(),
        name='post_detail'),
)
