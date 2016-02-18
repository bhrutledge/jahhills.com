from datetime import datetime

from django.test import TestCase
from django.utils import timezone

from core.tests.models import (
    FieldsTestMixin, PublishTestMixin, TitleTestMixin)

from ..models import Post
from .factories import DraftPostFactory, PublishedPostFactory


class PostTestCase(FieldsTestMixin, PublishTestMixin, TitleTestMixin,
                   TestCase):

    model = Post
    factory = DraftPostFactory
    required_fields = ['title', 'slug']

    def test_ordered_by_date(self):
        draft = DraftPostFactory.create()

        first = PublishedPostFactory.create(
            publish_on=datetime(2014, 7, 22, tzinfo=timezone.utc))

        old = PublishedPostFactory.create(
            publish_on=datetime(2014, 7, 21, tzinfo=timezone.utc))

        new = PublishedPostFactory.create(
            publish_on=datetime(2014, 7, 23, tzinfo=timezone.utc))

        self.assertEqual(list(Post.objects.all()), [draft, new, first, old])
