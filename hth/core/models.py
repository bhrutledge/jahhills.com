from django.db import models
from django.core.urlresolvers import reverse
from django.utils import timezone


class PublishedQuerySet(models.QuerySet):
    """
    Provides additional filters for ``PublishedModel``.
    """

    def published(self):
        """
        Returns a ``QuerySet`` of published objects.
        """

        return self.filter(publish=True)


class PublishedModel(models.Model):
    """
    Provides common fields and a manager for publishable content.
    """

    publish = models.BooleanField(
        default=False,
        help_text="Sets 'publish on' to now unless already set.")
    publish_on = models.DateTimeField(blank=True, null=True)

    objects = PublishedQuerySet.as_manager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Sets ``publish_on`` to now for a newly-published object.
        """

        # TODO: Make publish a method, setting publish_on?

        if self.publish and not self.publish_on:
            self.publish_on = timezone.now()

        super().save(*args, **kwargs)


class TitledModel(models.Model):
    """
    Provides a title and unique URL for publishable content.
    """

    title = models.CharField(max_length=200)
    slug = models.SlugField(
        unique=True, help_text="A unique label, used in URLs.")

    class Meta:
        abstract = True

    def __str__(self):
        """
        Returns the ``title``.
        """
        return self.title

    def get_absolute_url(self):
        """
        Returns the ``slug``-based URL.
        """
        return reverse(self._meta.model_name + '_detail', args=[self.slug])
