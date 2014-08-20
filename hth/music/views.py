from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Release, Song, Video


class ReleaseListView(ListView):
    """
    Renders a list of published ``Release``s.
    """
    queryset = Release.published.all()


class ReleaseDetailView(DetailView):
    """
    Renders a single published ``Release``.
    """
    queryset = Release.published.all()


class SongListView(ListView):
    """
    Renders a list of published ``Song``s.
    """
    queryset = Song.published.all()


class SongDetailView(DetailView):
    """
    Renders a single published ``Song``.
    """
    queryset = Song.published.all()


class VideoListView(ListView):
    """
    Renders a list of published ``Video``s.
    """
    queryset = Video.published.all()


class VideoDetailView(DetailView):
    """
    Renders a single published ``Video``.
    """
    queryset = Video.published.all()
