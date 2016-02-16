from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone


class FieldsTestMixin():
    """
    Provides tests of required and optional fields.

    Subclasses are responsible for defining class attributes.

    Attributes:
        model: The subclass of ``django.db.models.Model`` being tested.
        required_fields: Required field names and default values::

            {'title': 'Content Title', 'slug': 'content-title'}

        optional_fields: Optional field names and default values::

            {'description': 'A long description'}
    """

    def build_model(self, **kwargs):
        """
        Build a new instance of ``model``, initialized with
        ``required_fields``.
        """
        fields = dict(self.required_fields)
        fields.update(kwargs)
        return self.model(**fields)

    def create_model(self, **kwargs):
        """
        Build and save a new instance of ``model``, initialized with
        ``required_fields``.
        """
        m = self.build_model(**kwargs)
        m.save()
        return m

    def test_errors_on_required_fields(self):
        with self.assertRaises(ValidationError) as cm:
            self.model().full_clean()

        required_fields = set(self.required_fields.keys())
        blank_fields = set(cm.exception.message_dict.keys())
        self.assertEquals(required_fields, blank_fields)

    def test_save_with_required_fields(self):
        try:
            m = self.build_model()
            m.full_clean()
            m.save()
        except (TypeError, ValidationError):
            raise AssertionError

        m1 = self.model.objects.first()
        self.assertEqual(m, m1)

    def test_save_with_all_fields(self):
        try:
            m = self.build_model(**self.optional_fields)
            m.full_clean()
            m.save()
        except (TypeError, ValidationError):
            raise AssertionError


class PublishTestMixin():
    """
    Provides tests for subclasses of ``PublishedModel``.

    Subclasses must also inherit ``FieldsTestMixin``.
    """

    def test_can_publish(self):
        now = timezone.now()
        p = self.create_model(publish=True)

        self.assertTrue(p.publish)
        self.assertEqual(p.publish_on.date(), now.date())

        p = self.model.objects.first()
        self.assertTrue(p.publish)
        self.assertEqual(p.publish_on.date(), now.date())

    def test_draft_by_default(self):
        p = self.create_model()

        self.assertFalse(p.publish)
        self.assertIsNone(p.publish_on)

    def test_can_set_date(self):
        y2k = datetime(2000, 1, 1, tzinfo=timezone.utc)
        p = self.create_model(publish_on=y2k)

        p = self.model.objects.first()
        self.assertEqual(p.publish_on, y2k)

    def test_published_filter(self):
        p = self.create_model(publish=True, slug='published')
        d = self.create_model()

        objects = list(self.model.objects.all())
        self.assertIn(p, objects)
        self.assertIn(d, objects)

        published = list(self.model.objects.published())
        self.assertIn(p, published)
        self.assertNotIn(d, published)


class SlugTestMixin():
    """
    Provides tests for subclasses of ``SlugModel``.

    Subclasses must also inherit ``FieldsTestMixin``.
    """

    def test_slug_must_be_unique(self):
        self.create_model(slug='test')
        with self.assertRaises(IntegrityError):
            self.create_model(slug='test')

    def test_str_is_slug(self):
        p = self.build_model(slug='test')
        self.assertEqual(str(p), 'test')
