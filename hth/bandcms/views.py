from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Post


class PostListView(ListView):
    queryset = Post.published.all()


class PostDetailView(DetailView):
    queryset = Post.published.all()

