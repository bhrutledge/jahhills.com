from django.conf.urls import url

from . import views

# TODO: post_patterns = [list_url(Post), detail_url(Post)]
# TODO: Use namespaces?

urlpatterns = [
    url(r'^$',
        views.PostListView.as_view(),
        name='post_list'),
    url(r'^(?P<slug>[-_\w]+)/$',
        views.PostDetailView.as_view(),
        name='post_detail'),
]
