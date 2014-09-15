from datetime import datetime

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone

from core.models import PublishedModel
from ..models import Post


class PostTestCase(TestCase):

    def test_can_be_published(self):
        self.assertTrue(issubclass(Post, PublishedModel))

    def test_required_fields(self):
        required_fields = set(['title', 'slug'])

        with self.assertRaises(ValidationError) as cm:
            Post().full_clean()

        blank_fields = set(cm.exception.message_dict.keys())
        self.assertEquals(required_fields, blank_fields)

    def test_can_be_saved(self):
        p = Post(title='First', slug='first')
        p.full_clean()
        p.save()

        p1 = Post.objects.get(slug='first')
        self.assertEqual(p, p1)

    def test_can_have_body(self):
        p = Post(title='First', slug='first', body='Content')

        # Shouldn't raise exception
        p.full_clean()
        p.save()

    def test_ordered_by_date(self):
        draft = Post.objects.create(title='Draft', slug='draft')

        first = Post.objects.create(
            title='First', slug='first', publish=True,
            publish_on=datetime(2014, 7, 22, tzinfo=timezone.utc))

        old = Post.objects.create(
            title='Old', slug='old', publish=True,
            publish_on=datetime(2014, 7, 21, tzinfo=timezone.utc))

        new = Post.objects.create(
            title='New', slug='new', publish=True,
            publish_on=datetime(2014, 7, 23, tzinfo=timezone.utc))

        self.assertEqual(list(Post.objects.all()), [draft, new, first, old])
