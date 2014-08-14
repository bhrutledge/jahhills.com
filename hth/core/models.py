from django.db import models
from django.utils import timezone


class PublishedManager(models.Manager):

    # TODO: Use published() method instead, and make this the default manager?

    def get_queryset(self):
        # TODO: publish_on <= timezone.now()?
        return super().get_queryset().filter(publish=True)


class PublishedModel(models.Model):
    slug = models.SlugField(unique=True)
    # TODO: Just use publish_on
    publish = models.BooleanField(default=False)
    publish_on = models.DateTimeField(blank=True, null=True)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        abstract = True

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        if self.publish and not self.publish_on:
            self.publish_on = timezone.now()
        super().save(*args, **kwargs)

