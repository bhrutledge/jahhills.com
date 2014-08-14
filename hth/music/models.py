from django.db import models
from django.core.urlresolvers import reverse
from core.models import PublishedModel


class Release(PublishedModel):
    title = models.CharField(max_length=200)
    date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)
    credits = models.TextField(blank=True)

    @property
    def tracks(self):
        return self.song_set.filter(publish=True).order_by('track')

    @property
    def videos(self):
        return self.video_set.filter(publish=True)

    def get_absolute_url(self):
        return reverse('release_detail', args=[self.slug])

    class Meta:
        ordering = ['-date']

