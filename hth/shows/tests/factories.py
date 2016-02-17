from datetime import date, timedelta
from random import randrange

import factory
import factory.fuzzy


class VenueFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'shows.Venue'

    name = factory.Sequence(lambda n: 'Venue %d' % n)
    city = factory.Sequence(lambda n: 'City %d' % n)
    website = factory.Sequence(lambda n: 'http://venue-%d.dev' % n)


class DraftGigFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'shows.Gig'

    date = factory.fuzzy.FuzzyDate(date(2000, 1, 1))
    venue = factory.SubFactory(VenueFactory)
    description = factory.fuzzy.FuzzyText(length=100)
    details = factory.fuzzy.FuzzyText(length=100)


class PublishedGigFactory(DraftGigFactory):

    publish = True


class UpcomingGigFactory(PublishedGigFactory):

    # Pick a random date from today through next year
    date = factory.LazyAttribute(
        lambda obj: date.today() + timedelta(days=randrange(365)))

    @classmethod
    def create_batch(cls, size, **kwargs):
        batch = super().create_batch(size, **kwargs)
        return sorted(batch, key=lambda x: x.date)


class PastGigFactory(PublishedGigFactory):

    # Pick a random date from yesterday through 10 years ago
    date = factory.LazyAttribute(
        lambda obj: date.today() - timedelta(days=randrange(1, 3650)))

    @classmethod
    def create_batch(cls, size, **kwargs):
        batch = super().create_batch(size, **kwargs)
        return sorted(batch, key=lambda x: x.date, reverse=True)
