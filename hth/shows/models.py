from django.db import models
from django.core.urlresolvers import reverse
from core.models import PublishedModel


class Gig(PublishedModel):
    """
    Stores a show, aka concert.
    """

    date = models.DateField()
    venue = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    description = models.TextField(
        blank=True, help_text="Type of gig, band line-up, video links, etc.")
    details = models.TextField(
        blank=True, help_text="Start time, cost, ticket and venue links, etc.")

    class Meta:
        ordering = ['-date']
