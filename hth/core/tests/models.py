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
        factory: A subclass of ``factory.django.DjangoModelFactory`` for
            ``model``, with defaults for required and optional fields.
        required_fields: A list of required field names.
    """

    def test_errors_on_required_fields(self):
        with self.assertRaises(ValidationError) as cm:
            self.model().full_clean()

        blank_fields = cm.exception.message_dict.keys()
        self.assertEquals(set(self.required_fields), set(blank_fields))

    def test_save_with_all_fields(self):
        try:
            m = self.factory.create()
            m.full_clean()
        except (TypeError, ValidationError):
            raise AssertionError


class PublishTestMixin():
    """
    Provides tests for subclasses of ``PublishedModel``.

    Subclasses must also inherit ``FieldsTestMixin``.
    """

    def test_can_publish(self):
        now = timezone.now()
        p = self.factory.create(publish=True)

        self.assertTrue(p.publish)
        self.assertEqual(p.publish_on.date(), now.date())

        p = self.model.objects.first()
        self.assertTrue(p.publish)
        self.assertEqual(p.publish_on.date(), now.date())

    def test_draft_by_default(self):
        p = self.factory.create()

        self.assertFalse(p.publish)
        self.assertIsNone(p.publish_on)

    def test_can_set_date(self):
        y2k = datetime(2000, 1, 1, tzinfo=timezone.utc)
        p = self.factory.create(publish_on=y2k)

        p = self.model.objects.first()
        self.assertEqual(p.publish_on, y2k)

    def test_published_filter(self):
        p = self.factory.create(publish=True)
        d = self.factory.create()

        objects = list(self.model.objects.all())
        self.assertIn(p, objects)
        self.assertIn(d, objects)

        published = list(self.model.objects.published())
        self.assertIn(p, published)
        self.assertNotIn(d, published)


class TitleTestMixin():
    """
    Provides tests for subclasses of ``TitledModel``.

    Subclasses must also inherit ``FieldsTestMixin``.
    """

    def test_slug_must_be_unique(self):
        self.factory.create(slug='test')
        with self.assertRaises(IntegrityError):
            self.factory.create(slug='test')

    def test_str_is_title(self):
        p = self.factory.build(title='Test Title')
        self.assertEqual(str(p), 'Test Title')
