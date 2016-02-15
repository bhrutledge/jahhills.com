from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone


class FieldsTestMixin():

    def test_errors_on_required_fields(self):
        with self.assertRaises(ValidationError) as cm:
            self.model().full_clean()

        required_fields = set(self.required_fields.keys())
        blank_fields = set(cm.exception.message_dict.keys())
        self.assertEquals(required_fields, blank_fields)

    def test_save_with_required_fields(self):
        try:
            m = self.model(**self.required_fields)
            m.full_clean()
            m.save()
        except (TypeError, ValidationError):
            raise AssertionError

        m1 = self.model.objects.first()
        self.assertEqual(m, m1)

    def test_save_with_all_fields(self):
        try:
            m = self.model(**self.required_fields, **self.optional_fields)
            m.full_clean()
            m.save()
        except (TypeError, ValidationError):
            raise AssertionError


class PublishTestMixin():

    def test_can_publish(self):
        now = timezone.now()
        p = self.model.objects.create(publish=True, **self.required_fields)

        self.assertTrue(p.publish)
        self.assertEqual(p.publish_on.date(), now.date())

        p = self.model.objects.first()
        self.assertTrue(p.publish)
        self.assertEqual(p.publish_on.date(), now.date())

    def test_draft_by_default(self):
        p = self.model.objects.create(**self.required_fields)

        self.assertFalse(p.publish)
        self.assertIsNone(p.publish_on)

    def test_can_set_date(self):
        y2k = datetime(2000, 1, 1, tzinfo=timezone.utc)
        p = self.model.objects.create(publish_on=y2k, **self.required_fields)

        p = self.model.objects.first()
        self.assertEqual(p.publish_on, y2k)

    def test_published_filter(self):
        published_kwargs = dict(self.required_fields)
        published_kwargs['slug'] = 'published'

        p = self.model.objects.create(publish=True, **published_kwargs)
        d = self.model.objects.create(**self.required_fields)

        objects = list(self.model.objects.all())
        self.assertIn(p, objects)
        self.assertIn(d, objects)

        published = list(self.model.objects.published())
        self.assertIn(p, published)
        self.assertNotIn(d, published)


class SlugTestMixin():

    def test_slug_must_be_unique(self):
        kwargs = dict(self.required_fields)
        kwargs['slug'] = 'test'

        self.model.objects.create(**kwargs)
        with self.assertRaises(IntegrityError):
            self.model.objects.create(slug='test')

    def test_str_is_slug(self):
        kwargs = dict(self.required_fields)
        kwargs['slug'] = 'test'

        p = self.model(**kwargs)
        self.assertEqual(str(p), 'test')
