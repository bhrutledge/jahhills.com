from datetime import datetime

from django.test import TestCase
from django.db import IntegrityError
from django.utils import timezone

from .models import Published


# TODO: Use factory_boy
class PublishedTestCase(TestCase):

    def test_can_be_saved(self):
        m = Published(slug='test')
        m.full_clean()
        m.save()

        m1 = Published.objects.get(slug='test')
        self.assertEqual(m, m1)
        # TODO: Assert slug?

    def test_slug_must_be_unique(self):
        Published(slug='test').save()
        with self.assertRaises(IntegrityError):
            Published(slug='test').save()

    def test_str_is_slug(self):
        m = Published(slug='test')
        self.assertEqual(str(m), 'test')

    def test_can_publish(self):
        now = timezone.now()
        m = Published(slug='test', publish=True)
        m.save()

        self.assertTrue(m.publish)
        self.assertEqual(m.publish_on.date(), now.date())

        m = Published.objects.get(slug='test')
        self.assertTrue(m.publish)
        self.assertEqual(m.publish_on.date(), now.date())

    def test_draft_by_default(self):
        m = Published(slug='test')
        m.save()

        # TODO: assert publish is false
        self.assertIsNone(m.publish_on)

    def test_can_set_date(self):
        y2k = datetime(2000, 1, 1, tzinfo=timezone.utc)
        m = Published(slug='y2k', publish_on=y2k)
        m.save()

        m = Published.objects.get(slug='y2k')
        self.assertEqual(m.publish_on, y2k)

    def test_published_filter(self):
        p = Published(slug='published', publish=True)
        p.save()

        d = Published(slug='draft')
        d.save()

        published = list(Published.published.all())
        self.assertIn(p, published)
        self.assertNotIn(d, published)

