from datetime import datetime

from django.test import TestCase, override_settings
from django.utils import timezone
from django.core.urlresolvers import reverse

from ..models import AbstractCmsModel, Post


class ModelTestCase(TestCase):

    def test_post_is_cms_model(self):
        self.assertTrue(issubclass(Post, AbstractCmsModel))

    def test_can_save_post(self):
        p = Post(title='First', slug='first', body='Content')
        p.save()

        p1 = Post.objects.get(slug='first')
        self.assertEqual(p, p1)

    def test_body_can_be_empty(self):
        p = Post(title='First', slug='first', body='Content')
        p.full_clean()
        p.save()

    def test_posts_ordered_by_date(self):
        first = Post(title='First', slug='first',
                     publish_on=datetime(2014, 7, 22, tzinfo=timezone.utc))
        first.save()

        old = Post(title='Old', slug='old',
                   publish_on=datetime(2014, 7, 21, tzinfo=timezone.utc))
        old.save()

        new = Post(title='New', slug='new',
                   publish_on=datetime(2014, 7, 23, tzinfo=timezone.utc))
        new.save()

        draft = Post(title='Draft', slug='draft')
        draft.save()

        self.assertEqual(list(Post.objects.all()), [draft, new, first, old])

    @override_settings(ROOT_URLCONF='bandcms.urls.posts')
    def test_url_uses_slug(self):
        p = Post(title='First', slug='first')
        p.save()

        self.assertEqual(p.get_absolute_url(), '/first/')


@override_settings(ROOT_URLCONF='bandcms.urls.posts')
class UrlTestCase(TestCase):

    def setUp(self):
        publish = Post(title='Foo', slug='foo')
        publish.save()

        draft = Post(title='Draft', slug='draft', publish=False)
        draft.save()

    def test_can_view_published_posts(self):
        response = self.client.get(reverse('post_detail', args=['foo']))
        self.assertTemplateUsed(response, 'bandcms/post_detail.html')
        self.assertContains(response, 'Foo')

    def test_cant_view_draft_posts(self):
        response = self.client.get(reverse('post_detail', args=['draft']))
        self.assertEqual(response.status_code, 404)

    def test_list_shows_published_posts(self):
        response = self.client.get(reverse('post_list'))
        self.assertTemplateUsed(response, 'bandcms/post_list.html')
        self.assertContains(response, 'Foo')
        self.assertNotContains(response, 'Draft')

