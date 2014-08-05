from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse


class PublishedManager(models.Manager):

    def get_queryset(self):
        # TODO: publish_on <= now?
        return super().get_queryset().filter(publish=True)


class AbstractCmsModel(models.Model):
    slug = models.SlugField(unique=True)
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


class CmsModel(AbstractCmsModel):
    pass


class Post(AbstractCmsModel):
    title = models.CharField(max_length=200)
    body = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.slug])

    class Meta:
        ordering = ['publish', '-publish_on']


class Gig(AbstractCmsModel):
    date = models.DateField()
    venue = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    details = models.TextField(blank=True)

    class Meta:
        ordering = ['-date']


class Release(AbstractCmsModel):
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


class Song(AbstractCmsModel):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    credits = models.TextField(blank=True)
    lyrics = models.TextField(blank=True)
    release = models.ForeignKey(Release, blank=True, null=True)
    track = models.PositiveIntegerField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('song_detail', args=[self.slug])

    class Meta:
        ordering = ['title']


class Video(AbstractCmsModel):
    title = models.CharField(max_length=200)
    source_url = models.CharField(max_length=200, blank=True)
    embed_code = models.TextField(blank=True)
    description = models.TextField(blank=True)
    credits = models.TextField(blank=True)
    release = models.ForeignKey(Release, blank=True, null=True)

    class Meta:
        ordering = ['publish', '-publish_on']

    def get_absolute_url(self):
        return reverse('video_detail', args=[self.slug])
