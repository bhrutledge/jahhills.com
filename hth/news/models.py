from django.db import models
from django.core.urlresolvers import reverse
from core.models import PublishedModel


class Post(PublishedModel):
    title = models.CharField(max_length=200)
    body = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.slug])

    class Meta:
        ordering = ['publish', '-publish_on']

