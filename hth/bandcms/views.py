from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Post, Gig, Release, Song, Video


# TODO: PublishedListView and PublishedDetailView?


class PostListView(ListView):
    queryset = Post.published.all()


class PostDetailView(DetailView):
    queryset = Post.published.all()


class GigListView(ListView):
    queryset = Gig.published.all()


class GigDetailView(DetailView):
    queryset = Gig.published.all()


class ReleaseListView(ListView):
    queryset = Release.published.all()


class ReleaseDetailView(DetailView):
    queryset = Release.published.all()


class SongListView(ListView):
    queryset = Song.published.all()


class SongDetailView(DetailView):
    queryset = Song.published.all()


class VideoListView(ListView):
    queryset = Video.published.all()


class VideoDetailView(DetailView):
    queryset = Video.published.all()

