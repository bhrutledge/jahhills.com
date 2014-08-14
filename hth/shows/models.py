from django.db import models
from django.core.urlresolvers import reverse
from core.models import PublishedModel


# TODO: Add help text
class Gig(PublishedModel):
    date = models.DateField()
    venue = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    details = models.TextField(blank=True)

    class Meta:
        ordering = ['-date']

