from datetime import date, timedelta

from django.test import TestCase

from core.tests.models import FieldsTestMixin, PublishTestMixin

from ..models import Venue, Gig
from .factories import (VenueFactory, GigFactory, PublishedGigFactory,
                        PastGigFactory, UpcomingGigFactory)


def from_today(days=0):
    return date.today() + timedelta(days)


class VenueTestCase(FieldsTestMixin, TestCase):

    model = Venue
    factory = VenueFactory
    required_fields = ['name', 'city']

    def test_str_is_name_and_city(self):
        v = Venue(name='Venue', city='City', website='http://venue.com')
        self.assertEqual(str(v), 'Venue, City')

    def test_ordered_by_name_and_city(self):
        # Save out of order to test ordering
        v2 = VenueFactory.create(name='A', city='d')
        v1 = VenueFactory.create(name='A', city='c')
        v4 = VenueFactory.create(name='C', city='c')
        v3 = VenueFactory.create(name='B', city='c')

        self.assertEqual(list(Venue.objects.all()), [v1, v2, v3, v4])


class GigTestCase(FieldsTestMixin, PublishTestMixin, TestCase):

    model = Gig
    factory = GigFactory
    required_fields = ['date', 'venue']

    def test_str_is_date_and_venue(self):
        v = Venue.objects.create(name='Venue', city='City')
        g = Gig.objects.create(date='2014-07-25', venue=v)
        self.assertEqual(str(g), '2014-07-25, Venue, City')

    def test_ordered_by_date(self):
        # Save out of order to test ordering
        g2 = PublishedGigFactory.create(date='2014-07-25')
        g1 = PublishedGigFactory.create(date='2014-07-26')
        g3 = PublishedGigFactory.create(date='2014-07-24')

        self.assertEqual(list(Gig.objects.all()), [g1, g2, g3])

    def test_published_selects_venue(self):
        published_gigs = PublishedGigFactory.create_batch(5)
        expected_venues = [g.venue for g in published_gigs]

        with self.assertNumQueries(1):
            actual_venues = [g.venue for g in Gig.objects.published()]
            self.assertEqual(set(actual_venues), set(expected_venues))

    def test_upcoming(self):
        next_year = UpcomingGigFactory.create(date=from_today(365))
        tomorrow = UpcomingGigFactory.create(date=from_today(1))
        next_month = UpcomingGigFactory.create(date=from_today(30))
        today = UpcomingGigFactory.create(date=from_today())

        PastGigFactory.create_batch(5)
        GigFactory.create_batch(5)

        self.assertEqual(list(Gig.objects.upcoming().published()),
                         [today, tomorrow, next_month, next_year])

    def test_past(self):
        last_year = PastGigFactory.create(date=from_today(-365))
        yesterday = PastGigFactory.create(date=from_today(-1))
        last_month = PastGigFactory.create(date=from_today(-30))

        UpcomingGigFactory.create_batch(5)
        GigFactory.create_batch(5)

        self.assertEqual(list(Gig.objects.past().published()),
                         [yesterday, last_month, last_year])
