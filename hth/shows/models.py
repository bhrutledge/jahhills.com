from datetime import date

from django.db import models

from core.models import PublishedModel, PublishedQuerySet


class Venue(models.Model):
    """
    Stores a club, bar, festival, etc.
    """

    name = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    website = models.URLField(blank=True)

    class Meta:
        ordering = ['name', 'city']

    def __str__(self):
        return '{}, {}'.format(self.name, self.city)


class GigQuerySet(PublishedQuerySet):
    """
    Provides additional filters for ``Gig``.
    """

    def published(self):
        """
        Returns a ``QuerySet`` of published objects with related ``Venue``s.
        """
        return super().published().select_related('venue')

    def upcoming(self):
        """
        Returns a ``QuerySet`` of future ``Gig``s in ascending order.
        """
        return self.filter(date__gte=date.today()).reverse()

    def past(self):
        """
        Returns a ``QuerySet`` of past ``Gig``s in descending order.
        """
        return self.filter(date__lt=date.today())


class Gig(PublishedModel):
    """
    Stores a show, aka concert.
    """

    date = models.DateField()
    venue = models.ForeignKey(Venue)
    description = models.TextField(
        blank=True, help_text="Type of gig, band line-up, video links, etc.")
    details = models.TextField(
        blank=True, help_text="Start time, cost, ticket and venue links, etc.")

    objects = GigQuerySet.as_manager()

    class Meta:
        ordering = ['-date']
