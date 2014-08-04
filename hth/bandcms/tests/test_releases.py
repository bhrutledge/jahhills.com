from django.test import TestCase, override_settings
from django.core.urlresolvers import reverse

from ..models import AbstractCmsModel, Release


@override_settings(ROOT_URLCONF='bandcms.urls')
class ModelTestCase(TestCase):

    def test_release_is_cms_model(self):
        self.assertTrue(issubclass(Release, AbstractCmsModel))

    def test_can_save_release(self):
        r = Release(title='First', slug='first')
        r.save()

        r1 = Release.objects.get(slug='first')
        self.assertEqual(r, r1)

    def test_release_can_have_details(self):
        r = Release(title='First', slug='first', date='2014-08-01',
                    description='Description', credits='Credits')
        r.full_clean()
        r.save()

    def test_releases_ordered_by_date(self):
        first = Release(title='First', slug='first', date='2014-08-01')
        first.save()

        old = Release(title='Older', slug='older', date='2014-07-31')
        old.save()

        new = Release(title='Newer', slug='newer', date='2014-08-31')
        new.save()

        self.assertEqual(list(Release.objects.all()), [new, first, old])

    def test_url_uses_slug(self):
        r = Release(title='First', slug='first')
        r.save()

        self.assertEqual(r.get_absolute_url(), '/releases/first/')


@override_settings(ROOT_URLCONF='bandcms.urls')
class UrlTestCase(TestCase):

    def setUp(self):
        publish = Release(title='Published', slug='published', publish=True)
        publish.save()

        draft = Release(title='Draft', slug='draft')
        draft.save()

    def test_can_view_published_releases(self):
        response = self.client.get(reverse('release_detail', args=['published']))
        self.assertTemplateUsed(response, 'bandcms/release_detail.html')
        self.assertContains(response, 'Published')

    def test_cant_view_draft_releases(self):
        response = self.client.get(reverse('release_detail', args=['draft']))
        self.assertEqual(response.status_code, 404)

    def test_list_shows_published_releases(self):
        response = self.client.get(reverse('release_list'))
        self.assertTemplateUsed(response, 'bandcms/release_list.html')
        self.assertContains(response, 'Published')
        self.assertNotContains(response, 'Draft')

