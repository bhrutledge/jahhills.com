from datetime import datetime

from django.test import TestCase
from django.utils import timezone

from core.tests.models import (
    FieldsTestMixin, PublishTestMixin, TitleTestMixin)

from ..models import Post
from .factories import DraftPostFactory


class PostTestCase(FieldsTestMixin, PublishTestMixin, TitleTestMixin,
                   TestCase):

    model = Post
    factory = DraftPostFactory
    required_fields = ['title', 'slug']

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
