from django.db import models
from django.core.urlresolvers import reverse

from core.models import PublishedModel


class Release(PublishedModel):
    """
    Stores an album, EP, or other collection of ``Songs``s and ``Video``s.
    """

    title = models.CharField(max_length=200)
    date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)
    credits = models.TextField(blank=True)

    class Meta:
        ordering = ['-date']

    def get_absolute_url(self):
        """
        Returns the ``slug``-based URL.
        """
        return reverse('release_detail', args=[self.slug])

    @property
    def tracks(self):
        """
        Returns a ``QuerySet`` of published songs, ordered by track.
        """
        return self.song_set(manager='published').order_by('track')

    @property
    def videos(self):
        """
        Returns a ``QuerySet`` of published videos, ordered by publish time.
        """
        return self.video_set(manager='published').all()


class Song(PublishedModel):
    """
    Stores a song, optionally as a track on a ``Release``.
    """

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    credits = models.TextField(blank=True)
    lyrics = models.TextField(blank=True)
    release = models.ForeignKey(Release, blank=True, null=True)
    track = models.PositiveIntegerField(
        blank=True, null=True, help_text="The track number on 'release'.")

    class Meta:
        ordering = ['title']

    def get_absolute_url(self):
        """
        Returns the ``slug``-based URL.
        """
        return reverse('song_detail', args=[self.slug])


class Video(PublishedModel):
    """
    Stores an embeddable video, e.g. YouTube, optionally on a ``Release``.
    """

    title = models.CharField(max_length=200)
    source_url = models.CharField(max_length=200, blank=True)
    embed_code = models.TextField(blank=True)
    description = models.TextField(blank=True)
    credits = models.TextField(blank=True)
    release = models.ForeignKey(Release, blank=True, null=True)

    class Meta:
        ordering = ['publish', '-publish_on']

    def get_absolute_url(self):
        """
        Returns the ``slug``-based URL.
        """
        return reverse('video_detail', args=[self.slug])
