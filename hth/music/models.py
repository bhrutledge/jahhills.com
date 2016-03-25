from django.core.urlresolvers import reverse
from django.db import models

from embed_video import backends

from core.models import PublishedModel, TitledModel


class Release(PublishedModel, TitledModel):
    """
    Stores an album, EP, or other collection of ``Song``'s and ``Video``'s.
    """

    date = models.DateField(blank=True, null=True)
    cover_url = models.URLField(
        blank=True,
        help_text="A link to the cover art, at the highest desired resolution."
    )
    player_code = models.TextField(blank=True)
    description = models.TextField(blank=True)
    credits = models.TextField(blank=True)

    class Meta:
        ordering = ['-date']

    @property
    def tracks(self):
        """
        A ``QuerySet`` of published songs, ordered by track.
        """
        return self.song_set.published().order_by('track')

    @property
    def has_lyrics(self):
        """
        True iff any of the tracks have lyrics.
        """
        return any(t.lyrics for t in self.tracks)

    @property
    def videos(self):
        """
        A ``QuerySet`` of published videos, ordered by publish time.
        """
        return self.video_set.published()

    @property
    def press(self):
        """
        A ``QuerySet`` of published press, ordered by date.
        """
        return self.press_set.published()

    def get_lyrics_url(self):
        """
        Returns the ``slug``-based URL for the track lyrics.
        """
        return reverse('release_lyrics', args=[self.slug])


class Song(PublishedModel, TitledModel):
    """
    Stores a song, optionally as a track on a ``Release``.
    """

    player_code = models.TextField(blank=True)
    description = models.TextField(blank=True)
    credits = models.TextField(blank=True)
    lyrics = models.TextField(blank=True)
    release = models.ForeignKey(Release, blank=True, null=True)
    track = models.PositiveIntegerField(
        blank=True, null=True, help_text="The track number on 'release'.")

    class Meta:
        ordering = ['title']

    @property
    def has_details(self):
        """
        True iff any TextField is non-empty
        """
        return any([
            self.player_code, self.description, self.credits, self.lyrics
        ])


class Video(PublishedModel, TitledModel):
    """
    Stores an embeddable video, e.g. YouTube, optionally on a ``Release``.
    """

    source_url = models.URLField(blank=True)
    embed_code = models.TextField(blank=True)
    preview_url = models.URLField(
        blank=True,
        help_text=("A link to the preview image. "
                   "Try http://vidthumb.com or http://embed.ly/embed.")
    )
    description = models.TextField(blank=True)
    credits = models.TextField(blank=True)
    release = models.ForeignKey(Release, blank=True, null=True)

    class Meta:
        ordering = ['publish', '-publish_on']

    def save(self, *args, **kwargs):
        if self.source_url and not (self.preview_url and self.embed_code):
            try:
                backend = backends.detect_backend(self.source_url)
            except backends.UnknownBackendException:
                pass
            else:
                if not self.preview_url:
                    self.preview_url = backend.get_thumbnail_url()
                if not self.embed_code:
                    self.embed_code = backend.get_embed_code('', '')

        super().save(*args, **kwargs)


class Press(PublishedModel):
    """
    Stores a press quote, optionally on a ``Release``.
    """

    title = models.CharField(max_length=200)
    date = models.DateField()
    source_url = models.URLField(blank=True)
    body = models.TextField(blank=True, help_text='HTML')
    quote = models.BooleanField(default=True)
    release = models.ForeignKey(Release, blank=True, null=True)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'press'

    def __str__(self):
        return '{}, {}'.format(self.title, self.date)
