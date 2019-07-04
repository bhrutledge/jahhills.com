from datetime import date, datetime, timezone

import factory
import factory.fuzzy


class ReleaseFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'music.Release'

    slug = factory.Sequence(lambda n: 'release-%d' % n)
    title = factory.LazyAttribute(lambda obj: 'Release {}'.format(obj.date))
    description = factory.fuzzy.FuzzyText(length=100)
    credits = factory.fuzzy.FuzzyText(length=100)
    date = factory.fuzzy.FuzzyDate(date(2000, 1, 1))


class PublishedReleaseFactory(ReleaseFactory):

    publish = True
    publish_on = factory.fuzzy.FuzzyDateTime(
        datetime(2000, 1, 1, tzinfo=timezone.utc))

    @classmethod
    def create_batch(cls, size, **kwargs):
        batch = super().create_batch(size, **kwargs)
        return sorted(batch, key=lambda x: x.date, reverse=True)


class SongFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'music.Song'

    slug = factory.Sequence(lambda n: 'song-%d' % n)
    title = factory.fuzzy.FuzzyText(prefix='Song ')
    description = factory.fuzzy.FuzzyText(length=100)
    credits = factory.fuzzy.FuzzyText(length=100)
    lyrics = factory.fuzzy.FuzzyText(length=100)


class PublishedSongFactory(SongFactory):

    publish = True
    publish_on = factory.fuzzy.FuzzyDateTime(
        datetime(2000, 1, 1, tzinfo=timezone.utc))

    @classmethod
    def create_batch(cls, size, **kwargs):
        batch = super().create_batch(size, **kwargs)
        return sorted(batch, key=lambda x: x.title)


class VideoFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'music.Video'

    slug = factory.Sequence(lambda n: 'video-%d' % n)
    title = factory.fuzzy.FuzzyText(prefix='Video ')
    description = factory.fuzzy.FuzzyText(length=100)
    credits = factory.fuzzy.FuzzyText(length=100)


class PublishedVideoFactory(VideoFactory):

    publish = True
    publish_on = factory.fuzzy.FuzzyDateTime(
        datetime(2000, 1, 1, tzinfo=timezone.utc))

    @classmethod
    def create_batch(cls, size, **kwargs):
        batch = super().create_batch(size, **kwargs)
        return sorted(batch, key=lambda x: x.publish_on, reverse=True)


class PressFactory(factory.django.DjangoModelFactory):

    title = factory.fuzzy.FuzzyText(prefix='Press ')
    date = factory.fuzzy.FuzzyDate(date(2000, 1, 1))
    source_url = 'http://example.com'
    body = factory.fuzzy.FuzzyText(length=100)

    class Meta:
        model = 'music.Press'


class PublishedPressFactory(PressFactory):

    publish = True
    publish_on = factory.fuzzy.FuzzyDateTime(
        datetime(2000, 1, 1, tzinfo=timezone.utc))
