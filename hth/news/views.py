from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Post


class PostListView(ListView):
    """
    Renders a list of published ``Post``s.
    """
    queryset = Post.published.all()


class PostDetailView(DetailView):
    """
    Renders a single published ``Post``.
    """
    queryset = Post.published.all()
