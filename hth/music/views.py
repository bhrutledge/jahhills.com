from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Release, Song, Video


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

