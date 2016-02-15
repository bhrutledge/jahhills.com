from datetime import datetime

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone

from core.tests.models import (
    FieldsTestMixin, PublishTestMixin, SlugTestMixin)

from ..models import Post


class PostTestCase(FieldsTestMixin, PublishTestMixin, SlugTestMixin, TestCase):

    model = Post
    required_fields = {'title': 'Title', 'slug': 'title'}
    optional_fields = {'body': 'content'}

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
