from django.core.exceptions import ValidationError
from django.test import TestCase

from hth.core.tests.models import FieldsTestMixin, PublishTestMixin
from hth.core.tests.utils import from_today

from ..models import Venue, Gig
from .factories import (VenueFactory, GigFactory, PublishedGigFactory,
                        PastGigFactory, UpcomingGigFactory)


class VenueTestCase(FieldsTestMixin, TestCase):

    model = Venue
    factory = VenueFactory
    required_fields = ['name', 'city']

    def test_str_is_name_and_city(self):
        v = VenueFactory.build(name='Venue', city='City')
        self.assertEqual(str(v), 'Venue, City')

    def test_ordered_by_name_and_city(self):
        # Save out of order to test ordering
        v2 = VenueFactory.create(name='A', city='d')
        v1 = VenueFactory.create(name='A', city='c')
        v4 = VenueFactory.create(name='C', city='c')
        v3 = VenueFactory.create(name='B', city='c')

        self.assertEqual(list(Venue.objects.all()), [v1, v2, v3, v4])

    def test_add_place_details(self):
        kwargs = {
            'name': 'Great Scott',
            'city': 'Allston, MA',
            'website': 'http://www.greatscottboston.com/',
            'address': '1222 Commonwealth Avenue, Allston, MA 02134, USA',
            'latitude': 42.3500779,
            'longitude': -71.13060159999999,
        }

        try:
            v = VenueFactory.build(**kwargs)
            v.full_clean()
            v.save()
        except (TypeError, ValidationError):  # pragma: no cover
            raise AssertionError


class GigTestCase(FieldsTestMixin, PublishTestMixin, TestCase):

    model = Gig
    factory = GigFactory
    required_fields = ['date', 'venue']

    def test_str_is_date_and_venue(self):
        v = VenueFactory.build(name='Venue', city='City')
        g = GigFactory.build(date='2014-07-25', venue=v)
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
