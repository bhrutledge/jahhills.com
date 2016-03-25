from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Release, Song, Video, Press


class ReleaseListView(ListView):
    """
    Renders a list of published ``Release``'s.
    """
    queryset = Release.objects.published()


class ReleaseDetailView(DetailView):
    """
    Renders a single published ``Release``.
    """
    queryset = Release.objects.published()


class ReleaseLyricsView(ReleaseDetailView):
    """
    Renders lyrics of published ``Songs``'s for a ``Release``.
    """
    template_name = 'music/release_lyrics.html'


class SongListView(ListView):
    """
    Renders a list of published ``Song``'s.
    """
    queryset = Song.objects.published()


class SongDetailView(DetailView):
    """
    Renders a single published ``Song``.
    """
    queryset = Song.objects.published()


class VideoListView(ListView):
    """
    Renders a list of published ``Video``'s.
    """
    queryset = Video.objects.published()


class VideoDetailView(DetailView):
    """
    Renders a single published ``Video``.
    """
    queryset = Video.objects.published()


class PressListView(ListView):
    """
    Renders a list of published ``Press``.
    """
    queryset = Press.objects.published()
