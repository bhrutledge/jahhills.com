from datetime import datetime

from django.test import TestCase
from django.db import IntegrityError
from django.utils import timezone

from ..models import CmsModel


# TODO: Make this a base class, subclass for each model?
# TODO: Look at ddt and/or nose generators
class CmsModelTestCase(TestCase):

    def test_model_can_be_saved(self):
        m = CmsModel(slug='test')
        m.full_clean()
        m.save()

        CmsModel.objects.get(slug='test')
        # TODO: assert slug is 'test'

    def test_slug_is_unique(self):
        CmsModel(slug='test').save()
        with self.assertRaises(IntegrityError):
            CmsModel(slug='test').save()

    def test_str_is_slug(self):
        m = CmsModel(slug='test')
        self.assertEqual(str(m), 'test')

    def test_can_publish(self):
        now = timezone.now()
        m = CmsModel(slug='test', publish=True)
        m.save()

        self.assertTrue(m.publish)
        self.assertEqual(m.publish_on.date(), now.date())

        m = CmsModel.objects.get(slug='test')
        self.assertTrue(m.publish)
        self.assertEqual(m.publish_on.date(), now.date())

    def test_draft_by_default(self):
        m = CmsModel(slug='test')
        m.save()

        # TODO: assert publish is false
        self.assertIsNone(m.publish_on)

    def test_can_set_date(self):
        y2k = datetime(2000, 1, 1, tzinfo=timezone.utc)
        m = CmsModel(slug='y2k', publish_on=y2k)
        m.save()

        m = CmsModel.objects.get(slug='y2k')
        self.assertEqual(m.publish_on, y2k)

    def test_published_filter(self):
        p = CmsModel(slug='published', publish=True)
        p.save()

        d = CmsModel(slug='draft')
        d.save()

        published = list(CmsModel.published.all())
        self.assertIn(p, published)
        self.assertNotIn(d, published)

