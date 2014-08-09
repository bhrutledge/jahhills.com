from datetime import datetime

from django.test import TestCase, override_settings
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.utils import timezone

from bandcms.tests.utils import today_str
from ..models import Gig


class GigTestCase(TestCase):

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
        # TODO: Assert slug?

    def test_slug_must_be_unique(self):
        g = Gig(date='2014-07-24', slug='test', venue='Venue', city='City')
        g.full_clean()
        g.save()

        with self.assertRaises(IntegrityError):
            g = Gig(date='2014-07-24', slug='test', venue='Venue', city='City')
            g.save()

    def test_str_is_slug(self):
        g = Gig(date='2014-07-24', slug='test', venue='Venue', city='City')
        self.assertEqual(str(g), 'test')

    def test_can_publish(self):
        now = timezone.now()
        g = Gig(date='2014-07-24', slug='test', venue='Venue', city='City',
                publish=True)
        g.full_clean()
        g.save()

        self.assertTrue(g.publish)
        self.assertEqual(g.publish_on.date(), now.date())

        g = Gig.objects.get(slug='test')
        self.assertTrue(g.publish)
        self.assertEqual(g.publish_on.date(), now.date())

    def test_draft_by_default(self):
        g = Gig(date='2014-07-24', slug='test', venue='Venue', city='City')
        g.full_clean()
        g.save()

        self.assertFalse(g.publish)
        self.assertIsNone(g.publish_on)

    def test_can_set_date(self):
        y2k = datetime(2000, 1, 1, tzinfo=timezone.utc)
        g = Gig(date='2014-07-24', slug='test', venue='Venue', city='City',
                publish_on=y2k)
        g.full_clean()
        g.save()

        g = Gig.objects.get(slug='test')
        self.assertEqual(g.publish_on, y2k)

    def test_published_filter(self):
        publish = Gig(date='2014-07-24', slug='published',
                      venue='Venue', city='City', publish=True)
        publish.full_clean()
        publish.save()

        draft = Gig(date='2014-07-25', slug='draft',
                    venue='Venue', city='City')
        draft.full_clean()
        draft.save()

        published = list(Gig.published.all())
        self.assertIn(publish, published)
        self.assertNotIn(draft, published)

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


@override_settings(ROOT_URLCONF='bandcms.urls')
class ViewTestCase(TestCase):

    def setUp(self):
        today = today_str()
        tomorrow = today_str(1)
        yesterday = today_str(-1)

        Gig(date=today, slug=today, venue='Today', city='c',
            publish=True).save()
        Gig(date=tomorrow, slug=tomorrow, venue='Tomorrow', city='c',
            publish=True).save()
        Gig(date=yesterday, slug=yesterday, venue='Yesterday', city='c',
            publish=True).save()
        Gig(date=today, slug=today+'-d', venue='Draft', city='c').save()

    def test_list_name(self):
        self.assertEqual(reverse('gig_list'), '/gigs/')

    def test_list_shows_published_gigs(self):
        response = self.client.get('/gigs/')
        self.assertTemplateUsed(response, 'bandcms/gig_list.html')

        self.assertContains(response, 'Today')
        self.assertContains(response, 'Tomorrow')
        self.assertContains(response, 'Yesterday')
        self.assertNotContains(response, 'Draft')

