from datetime import date, timedelta
from random import randrange

import factory
import factory.fuzzy


class VenueFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'shows.Venue'

    name = factory.Sequence(lambda n: 'Venue %d' % n)
    city = factory.Sequence(lambda n: 'City %d' % n)


class DraftGigFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'shows.Gig'

    slug = factory.Sequence(lambda n: 'gig-%d' % n)
    date = factory.fuzzy.FuzzyDate(date(2000, 1, 1))
    venue = factory.SubFactory(VenueFactory)
    description = factory.fuzzy.FuzzyText(length=100)
    details = factory.fuzzy.FuzzyText(length=100)


class PublishedGigFactory(DraftGigFactory):

    publish = True


class UpcomingGigFactory(PublishedGigFactory):

    class Meta:
        exclude = ('days',)

    # Pick a random date from today through next year
    days = randrange(365)
    date = factory.LazyAttribute(
        lambda obj: date.today() + timedelta(days=obj.days))

    @classmethod
    def create_batch(cls, size, **kwargs):
        batch = super().create_batch(size, **kwargs)
        return sorted(batch, key=lambda x: x.date)


class PastGigFactory(PublishedGigFactory):

    class Meta:
        exclude = ('days',)

    # Pick a random date from yesterday through 10 years ago
    days = randrange(1, 3650)
    date = factory.LazyAttribute(
        lambda obj: date.today() - timedelta(days=obj.days))

    @classmethod
    def create_batch(cls, size, **kwargs):
        batch = super().create_batch(size, **kwargs)
        return sorted(batch, key=lambda x: x.date, reverse=True)
