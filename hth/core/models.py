from django.db import models
from django.utils import timezone


class PublishedManager(models.Manager):
    """Alternate manager for `PublishedModel`."""

    # TODO: Better to have published() method and make this the default manager?

    def get_queryset(self):
        """Returns a `QuerySet` of published objects."""

        # TODO: publish_on <= timezone.now()?
        return super().get_queryset().filter(publish=True)


class PublishedModel(models.Model):
    """Base class for content type models."""

    slug = models.SlugField(unique=True,
                            help_text="A unique label, used in URLs.")
    publish = models.BooleanField(default=False)
    publish_on = models.DateTimeField(blank=True, null=True)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        abstract = True

    def __str__(self):
        """Returns the `slug`."""

        return self.slug

    def save(self, *args, **kwargs):
        """Sets `publish_on` to now for a newly-published object."""

        # TODO: Make publish a method, setting publish_on?

        if self.publish and not self.publish_on:
            self.publish_on = timezone.now()

        super().save(*args, **kwargs)

