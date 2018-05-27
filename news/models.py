from django.db import models

from core.models import PublishedModel, TitledModel


class Post(PublishedModel, TitledModel):
    """
    Stores a news post.
    """

    body = models.TextField(blank=True, help_text="HTML")

    class Meta:
        ordering = ['publish', '-publish_on']
