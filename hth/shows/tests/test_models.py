from django.test import TestCase
from django.core.exceptions import ValidationError

from core.tests.utils import today_str
from ..models import PublishedModel, Venue, Gig


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
        v1 = Venue(name='A', city='c')
        v2 = Venue(name='A', city='d')
        v3 = Venue(name='B', city='c')
        v4 = Venue(name='C', city='c')

        # Save out of order to test ordering
        v2.save()
        v1.save()
        v4.save()
        v3.save()

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
        g1 = Gig(date='2014-07-26', slug='g1', venue=self.venue)
        g2 = Gig(date='2014-07-25', slug='g2', venue=self.venue)
        g3 = Gig(date='2014-07-24', slug='g3', venue=self.venue)

        # Save out of order to test ordering
        g2.save()
        g1.save()
        g3.save()

        self.assertEqual(list(Gig.objects.all()), [g1, g2, g3])

    def test_upcoming(self):
        next_year = Gig.objects.create(date=today_str(365), slug='next-year',
                                        venue=self.venue, publish=True)
        tomorrow = Gig.objects.create(date=today_str(1), slug='tomorrow',
                                      venue=self.venue, publish=True)
        next_month = Gig.objects.create(date=today_str(30), slug='next-month',
                                        venue=self.venue, publish=True)
        today = Gig.objects.create(date=today_str(), slug='today',
                                   venue=self.venue, publish=True)
        last_month = Gig.objects.create(date=today_str(-30), slug='last-month',
                                  venue=self.venue, publish=True)
        draft = Gig.objects.create(date=today_str(30), slug='draft',
                                   venue=self.venue)

        self.assertEqual(list(Gig.objects.published().upcoming()),
                         [today, tomorrow, next_month, next_year])

    def test_past(self):
        last_year = Gig.objects.create(date=today_str(-365), slug='last-year',
                                        venue=self.venue, publish=True)
        tomorrow = Gig.objects.create(date=today_str(1), slug='tomorrow',
                                      venue=self.venue, publish=True)
        yesterday = Gig.objects.create(date=today_str(-1), slug='yesterday',
                                      venue=self.venue, publish=True)
        last_month = Gig.objects.create(date=today_str(-30), slug='last-month',
                                        venue=self.venue, publish=True)
        today = Gig.objects.create(date=today_str(), slug='today',
                                   venue=self.venue, publish=True)
        draft = Gig.objects.create(date=today_str(30), slug='draft',
                                   venue=self.venue)

        self.assertEqual(list(Gig.objects.published().past()),
                         [yesterday, last_month, last_year])
