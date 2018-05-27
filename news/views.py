from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Post


class PostListView(ListView):
    """
    Renders a list of published ``Post``'s.
    """
    queryset = Post.objects.published()


class PostDetailView(DetailView):
    """
    Renders a single published ``Post``.
    """
    queryset = Post.objects.published()
