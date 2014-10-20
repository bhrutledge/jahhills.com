from django.test import TestCase
from django.core.exceptions import ValidationError

from ..models import PublishedModel, Venue, Gig
from .factories import (
    DraftGigFactory, PublishedGigFactory, PastGigFactory, UpcomingGigFactory)


class VenueTestCase(TestCase):

    def test_can_be_saved(self):
        v = Venue(name='Venue', city='City')
        v.full_clean()
        v.save()

        v1 = Venue.objects.first()
        self.assertEqual(v, v1)

    def test_required_fields(self):
        required_fields = set(['name', 'city'])

        with self.assertRaises(ValidationError) as cm:
            Venue().full_clean()

        blank_fields = set(cm.exception.message_dict.keys())
        self.assertEquals(required_fields, blank_fields)

    def test_can_have_details(self):
        v = Venue(name='Venue', city='City', website='http://venue.com')
        v.full_clean()
        v.save()

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


class GigTestCase(TestCase):

    def setUp(self):
        self.venue = Venue.objects.create(name='Venue', city='City')

    def test_can_be_published(self):
        self.assertTrue(issubclass(Gig, PublishedModel))

    def test_required_fields(self):
        required_fields = set(['date', 'slug', 'venue'])

        with self.assertRaises(ValidationError) as cm:
            Gig().full_clean()

        blank_fields = set(cm.exception.message_dict.keys())
        self.assertEquals(required_fields, blank_fields)

    def test_can_be_saved(self):
        g = Gig(date='2014-07-24', slug='test', venue=self.venue)
        g.full_clean()
        g.save()

        g1 = Gig.objects.get(slug='test')
        self.assertEqual(g, g1)

    def test_can_have_details(self):
        g = Gig(date='2014-07-24', slug='test', venue=self.venue,
                description='Description', details='Details')
        g.full_clean()
        g.save()

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
        next_year = UpcomingGigFactory.create(days=365)
        tomorrow = UpcomingGigFactory.create(days=1)
        next_month = UpcomingGigFactory.create(days=30)
        today = UpcomingGigFactory.create(days=0)

        PastGigFactory.create_batch(5)
        DraftGigFactory.create_batch(5)

        self.assertEqual(list(Gig.objects.upcoming().published()),
                         [today, tomorrow, next_month, next_year])

    def test_past(self):
        last_year = PastGigFactory.create(days=365)
        yesterday = PastGigFactory.create(days=1)
        last_month = PastGigFactory.create(days=30)

        UpcomingGigFactory.create_batch(5)
        DraftGigFactory.create_batch(5)

        self.assertEqual(list(Gig.objects.past().published()),
                         [yesterday, last_month, last_year])
