from django.test import TestCase
from django.core.urlresolvers import reverse

from ..models import Release


class ReleaseTestCase(TestCase):

    def setUp(self):
        self.publish = Release(title='Publish', slug='publish', publish=True)
        self.publish.save()

        self.draft = Release(title='Draft', slug='draft')
        self.draft.save()

    def test_url_uses_slug(self):
        self.assertEqual(self.publish.get_absolute_url(), '/music/publish/')

    def test_can_view_published_releases(self):
        response = self.client.get('/music/publish/')
        self.assertTemplateUsed(response, 'music/release_detail.html')
        self.assertContains(response, 'Publish')

    def test_cant_view_draft_releases(self):
        response = self.client.get('/music/draft/')
        self.assertEqual(response.status_code, 404)

    def test_list_shows_publish_releases(self):
        response = self.client.get('/music/')
        self.assertTemplateUsed(response, 'music/release_list.html')
        self.assertContains(response, 'Publish')
        self.assertNotContains(response, 'Draft')

