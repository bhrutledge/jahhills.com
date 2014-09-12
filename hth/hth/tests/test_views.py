from django.test import TestCase
from django.core.urlresolvers import reverse


from news.models import Post
from news.tests.factories import PostFactory, PublishedPostFactory


class HomeTestCase(TestCase):

    def test_name(self):
        self.assertEqual(reverse('home_page'), '/')

    def test_uses_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home_page.html')

    def test_returns_last_post(self):
        PublishedPostFactory.create_batch(5)
        PostFactory.create_batch(5)

        response = self.client.get('/')
        post = response.context['post']

        self.assertEqual(post, Post.objects.published().first())
