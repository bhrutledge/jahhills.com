from datetime import date, timedelta

from django.test import TestCase

from core.tests.models import (
    FieldsTestMixin, PublishTestMixin, SlugTestMixin)

from ..models import Venue, Gig
from .factories import (
    DraftGigFactory, PublishedGigFactory, PastGigFactory, UpcomingGigFactory)


def from_today(days=0):
    return date.today() + timedelta(days)


class VenueTestCase(FieldsTestMixin, TestCase):

    model = Venue
    required_fields = {'name': 'Venue', 'city': 'City'}
    optional_fields = {'website': 'http://venue.com'}

    def test_str_is_name_and_city(self):
        v = Venue(name='Venue', city='City', website='http://venue.com')
        self.assertEqual(str(v), 'Venue, City')

    def test_ordered_by_name_and_city(self):
        # Save out of order to test ordering
        v2 = Venue.objects.create(name='A', city='d')
        v1 = Venue.objects.create(name='A', city='c')
        v4 = Venue.objects.create(name='C', city='c')
        v3 = Venue.objects.create(name='B', city='c')

        self.assertEqual(list(Venue.objects.all()), [v1, v2, v3, v4])


class GigTestCase(FieldsTestMixin, PublishTestMixin, SlugTestMixin, TestCase):

    model = Gig

    @property
    def required_fields(self):
        return {'date': '2014-07-24', 'slug': 'test', 'venue': self.venue}

    optional_fields = {'description': 'Description', 'details': 'Details'}

    def setUp(self):
        self.venue = Venue.objects.create(name='Venue', city='City')

    def test_ordered_by_date(self):
        # Save out of order to test ordering
        g2 = Gig.objects.create(date='2014-07-25', slug='g2', venue=self.venue)
        g1 = Gig.objects.create(date='2014-07-26', slug='g1', venue=self.venue)
        g3 = Gig.objects.create(date='2014-07-24', slug='g3', venue=self.venue)

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
        DraftGigFactory.create_batch(5)

        self.assertEqual(list(Gig.objects.upcoming().published()),
                         [today, tomorrow, next_month, next_year])

    def test_past(self):
        last_year = PastGigFactory.create(date=from_today(-365))
        yesterday = PastGigFactory.create(date=from_today(-1))
        last_month = PastGigFactory.create(date=from_today(-30))

        UpcomingGigFactory.create_batch(5)
        DraftGigFactory.create_batch(5)

        self.assertEqual(list(Gig.objects.past().published()),
                         [yesterday, last_month, last_year])
