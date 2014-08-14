from django.test import TestCase
from django.core.urlresolvers import reverse

from ..models import Post


class ViewTestCase(TestCase):

    def setUp(self):
        self.publish = Post(title='Publish', slug='publish', publish=True)
        self.publish.save()

        self.draft = Post(title='Draft', slug='draft')
        self.draft.save()

    def test_url_uses_slug(self):
        self.assertEqual(self.publish.get_absolute_url(), '/news/publish/')

    def test_list_name(self):
        self.assertEqual(reverse('post_list'), '/news/')

    def test_detail_name(self):
        self.assertEqual(reverse('post_detail', args=['test']), '/news/test/')

    def test_can_view_published_news(self):
        response = self.client.get('/news/publish/')
        self.assertTemplateUsed(response, 'news/post_detail.html')
        self.assertContains(response, 'Publish')

    def test_cant_view_draft_news(self):
        response = self.client.get('/news/draft/')
        self.assertEqual(response.status_code, 404)

    def test_list_shows_published_news(self):
        response = self.client.get('/news/')
        self.assertTemplateUsed(response, 'news/post_list.html')
        self.assertContains(response, 'Publish')
        self.assertNotContains(response, 'Draft')

