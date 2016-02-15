from django.db import models

from core.models import PublishedModel, SlugModel


class Post(PublishedModel, SlugModel):
    """
    Stores a news post.
    """

    title = models.CharField(max_length=200)
    body = models.TextField(blank=True, help_text="HTML")

    class Meta:
        ordering = ['publish', '-publish_on']
