from datetime import date, timedelta

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


class UpcomingGigFactory(DraftGigFactory):

    publish = True
    date = factory.fuzzy.FuzzyDate(date.today() + timedelta(days=1),
                                   date.today() + timedelta(days=365))


class PastGigFactory(DraftGigFactory):

    publish = True
    date = factory.fuzzy.FuzzyDate(date(2000, 1, 1),
                                   date.today() - timedelta(days=1))
