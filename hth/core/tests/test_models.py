from datetime import datetime

from django.test import TestCase
from django.db import IntegrityError
from django.utils import timezone

from .models import Published


class PublishedTestCase(TestCase):

    def test_can_be_saved(self):
        p = Published(slug='test')
        p.full_clean()
        p.save()

        p1 = Published.objects.get(slug='test')
        self.assertEqual(p, p1)
        # TODO: Assert slug?

    def test_slug_must_be_unique(self):
        Published.objects.create(slug='test')
        with self.assertRaises(IntegrityError):
            Published.objects.create(slug='test')

    def test_str_is_slug(self):
        p = Published(slug='test')
        self.assertEqual(str(p), 'test')

    def test_can_publish(self):
        now = timezone.now()
        p = Published.objects.create(slug='test', publish=True)

        self.assertTrue(p.publish)
        self.assertEqual(p.publish_on.date(), now.date())

        p = Published.objects.get(slug='test')
        self.assertTrue(p.publish)
        self.assertEqual(p.publish_on.date(), now.date())

    def test_draft_by_default(self):
        p = Published.objects.create(slug='test')

        self.assertFalse(p.publish)
        self.assertIsNone(p.publish_on)

    def test_can_set_date(self):
        y2k = datetime(2000, 1, 1, tzinfo=timezone.utc)
        p = Published.objects.create(slug='y2k', publish_on=y2k)

        p = Published.objects.get(slug='y2k')
        self.assertEqual(p.publish_on, y2k)

    def test_published_filter(self):
        p = Published.objects.create(slug='published', publish=True)
        d = Published.objects.create(slug='draft')

        objects = list(Published.objects.all())
        self.assertIn(p, objects)
        self.assertIn(d, objects)

        published = list(Published.objects.published())
        self.assertIn(p, published)
        self.assertNotIn(d, published)
