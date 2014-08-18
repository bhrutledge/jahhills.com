from django.test import TestCase
from django.core.exceptions import ValidationError

from ..models import PublishedModel, Gig


class GigTestCase(TestCase):

    def test_can_be_published(self):
        self.assertTrue(issubclass(Gig, PublishedModel))

    def test_required_fields(self):
        required_fields = set(['date', 'slug', 'venue', 'city'])

        with self.assertRaises(ValidationError) as cm:
            Gig().full_clean()

        blank_fields = set(cm.exception.message_dict.keys())
        self.assertEquals(required_fields, blank_fields)

    def test_can_be_saved(self):
        g = Gig(date='2014-07-24', slug='test', venue='Venue', city='City')
        g.full_clean()
        g.save()

        g1 = Gig.objects.get(slug='test')
        self.assertEqual(g, g1)

    def test_can_have_details(self):
        g = Gig(date='2014-07-24', slug='test', venue='Venue', city='City',
                description='Description', details='Details')
        g.full_clean()
        g.save()

    def test_ordered_by_date(self):

        g1 = Gig(date='2014-07-26', slug='g1', venue='Venue', city='City')
        g2 = Gig(date='2014-07-25', slug='g2', venue='Venue', city='City')
        g3 = Gig(date='2014-07-24', slug='g3', venue='Venue', city='City')

        g2.save()
        g1.save()
        g3.save()

        self.assertEqual(list(Gig.objects.all()), [g1, g2, g3])

