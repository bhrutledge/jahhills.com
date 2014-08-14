from django.test import TestCase
from django.core.exceptions import ValidationError

from core.models import PublishedModel
from ..models import Release


class ReleaseTestCase(TestCase):

    def test_can_be_published(self):
        self.assertTrue(issubclass(Release, PublishedModel))

    def test_required_fields(self):
        required_fields = set(['title', 'slug'])

        with self.assertRaises(ValidationError) as cm:
            Release().full_clean()

        blank_fields = set(cm.exception.message_dict.keys())
        self.assertEquals(required_fields, blank_fields)

    def test_can_be_saved(self):
        r = Release(title='First', slug='first')
        r.full_clean()
        r.save()

        r1 = Release.objects.get(slug='first')
        self.assertEqual(r, r1)

    def test_can_have_details(self):
        r = Release(title='First', slug='first', date='2014-08-01',
                    description='Description', credits='Credits')
        r.full_clean()
        r.save()

    def test_ordered_by_date(self):
        first = Release(title='First', slug='first', date='2014-08-01')
        first.save()

        old = Release(title='Older', slug='older', date='2014-07-31')
        old.save()

        new = Release(title='Newer', slug='newer', date='2014-08-31')
        new.save()

        self.assertEqual(list(Release.objects.all()), [new, first, old])

