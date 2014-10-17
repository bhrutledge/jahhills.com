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
