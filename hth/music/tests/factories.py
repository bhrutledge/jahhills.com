from datetime import date, datetime, timezone

import factory
import factory.fuzzy


class DraftReleaseFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'music.Release'

    slug = factory.Sequence(lambda n: 'release-%d' % n)
    title = factory.Sequence(lambda n: 'Release %d' % n)
    description = factory.fuzzy.FuzzyText(length=100)


class PublishedReleaseFactory(DraftReleaseFactory):

    date = factory.fuzzy.FuzzyDate(date(2000, 1, 1))
    publish = True
    publish_on = factory.fuzzy.FuzzyDateTime(
        datetime(2000, 1, 1, tzinfo=timezone.utc))

    @classmethod
    def create_batch(cls, size, **kwargs):
        batch = super().create_batch(size, **kwargs)
        return sorted(batch, key=lambda x: x.date, reverse=True)


class DraftVideoFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'music.Video'

    slug = factory.Sequence(lambda n: 'video-%d' % n)
    title = factory.Sequence(lambda n: 'Video %d' % n)
    description = factory.fuzzy.FuzzyText(length=100)
    credits = factory.fuzzy.FuzzyText(length=100)


class PublishedVideoFactory(DraftVideoFactory):

    publish = True
    publish_on = factory.fuzzy.FuzzyDateTime(
        datetime(2000, 1, 1, tzinfo=timezone.utc))

    @classmethod
    def create_batch(cls, size, **kwargs):
        batch = super().create_batch(size, **kwargs)
        return sorted(batch, key=lambda x: x.publish_on, reverse=True)