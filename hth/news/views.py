from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.utils import timezone

from .models import Post


class PublishedQuerySetMixin():

    def get_queryset(self):
        # Delay call to now() by wrapping in function
        return super().get_queryset().filter(publish_on__lte=timezone.now())


class PostListView(PublishedQuerySetMixin, ListView):
    """
    Render a list of published posts
    """

    model = Post


class PostDetailView(PublishedQuerySetMixin, DetailView):
    """
    Render a 'detail' view for a published Post
    """

    model = Post

