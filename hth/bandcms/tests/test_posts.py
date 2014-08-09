from datetime import datetime

from django.test import TestCase, override_settings
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.utils import timezone

from ..models import Post


class PostTestCase(TestCase):

    def test_required_fields(self):
        required_fields = set(['title', 'slug'])

        with self.assertRaises(ValidationError) as cm:
            Post().full_clean()

        blank_fields = set(cm.exception.message_dict.keys())
        self.assertEquals(required_fields, blank_fields)

        # Shouldn't raise exception
        Post(title='First', slug='first').full_clean()

    def test_can_be_saved(self):
        p = Post(title='First', slug='first')
        p.full_clean()
        p.save()

        p1 = Post.objects.get(slug='first')
        self.assertEqual(p, p1)
        # TODO: Assert title and slug?

    def test_slug_must_be_unique(self):
        p = Post(title='Test', slug='test')
        p.full_clean()
        p.save()

        with self.assertRaises(IntegrityError):
            Post(title='Test', slug='test').save()

    def test_str_is_slug(self):
        p = Post(title='Test', slug='test')
        self.assertEqual(str(p), 'test')

    def test_can_publish(self):
        now = timezone.now()
        p = Post(title='Test', slug='test', publish=True)
        p.full_clean()
        p.save()

        self.assertTrue(p.publish)
        self.assertEqual(p.publish_on.date(), now.date())

        p = Post.objects.get(slug='test')
        self.assertTrue(p.publish)
        self.assertEqual(p.publish_on.date(), now.date())

    def test_draft_by_default(self):
        p = Post(title='Test', slug='test')
        p.full_clean()
        p.save()

        self.assertFalse(p.publish)
        self.assertIsNone(p.publish_on)

    def test_can_set_date(self):
        y2k = datetime(2000, 1, 1, tzinfo=timezone.utc)
        p = Post(title='Test', slug='test', publish_on=y2k)
        p.full_clean()
        p.save()

        p = Post.objects.get(slug='test')
        self.assertEqual(p.publish_on, y2k)

    def test_published_filter(self):
        publish = Post(title='Publish', slug='published', publish=True)
        publish.full_clean()
        publish.save()

        draft = Post(title='Draft', slug='draft')
        draft.full_clean()
        draft.save()

        published = list(Post.published.all())
        self.assertIn(publish, published)
        self.assertNotIn(draft, published)

    def test_can_have_body(self):
        p = Post(title='First', slug='first', body='Content')
        p.full_clean()
        p.save()
        # TODO: Assert body?

    def test_ordered_by_date(self):
        draft = Post(title='Draft', slug='draft')
        draft.save()

        first = Post(title='First', slug='first', publish=True,
                     publish_on=datetime(2014, 7, 22, tzinfo=timezone.utc))
        first.save()

        old = Post(title='Old', slug='old', publish=True,
                   publish_on=datetime(2014, 7, 21, tzinfo=timezone.utc))
        old.save()

        new = Post(title='New', slug='new', publish=True,
                   publish_on=datetime(2014, 7, 23, tzinfo=timezone.utc))
        new.save()

        self.assertEqual(list(Post.objects.all()), [draft, new, first, old])


@override_settings(ROOT_URLCONF='bandcms.urls')
class ViewTestCase(TestCase):

    def setUp(self):
        publish = Post(title='Publish', slug='publish', publish=True)
        publish.save()

        draft = Post(title='Draft', slug='draft')
        draft.save()

    def test_url_uses_slug(self):
        p = Post(title='First', slug='first')
        p.save()

        self.assertEqual(p.get_absolute_url(), '/posts/first/')

    def test_list_name(self):
        self.assertEqual(reverse('post_list'), '/posts/')

    def test_detail_name(self):
        self.assertEqual(reverse('post_detail', args=['test']), '/posts/test/')

    def test_can_view_published_posts(self):
        response = self.client.get('/posts/publish/')
        self.assertTemplateUsed(response, 'bandcms/post_detail.html')
        self.assertContains(response, 'Publish')

    def test_cant_view_draft_posts(self):
        response = self.client.get('/posts/draft/')
        self.assertEqual(response.status_code, 404)

    def test_list_shows_published_posts(self):
        response = self.client.get('/posts/')
        self.assertTemplateUsed(response, 'bandcms/post_list.html')
        self.assertContains(response, 'Publish')
        self.assertNotContains(response, 'Draft')

