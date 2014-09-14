from django.test import TestCase
from django.core.urlresolvers import reverse

from news.tests.factories import DraftPostFactory, PublishedPostFactory
from shows.tests.factories import (
    DraftGigFactory, PastGigFactory, UpcomingGigFactory)


class HomeTestCase(TestCase):

    def test_name(self):
        self.assertEqual(reverse('home_page'), '/')

    def test_uses_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home_page.html')

    def test_returns_latest_post(self):
        published_posts = PublishedPostFactory.create_batch(5)
        published_posts = sorted(published_posts,
                                 key=lambda x: x.publish_on,
                                 reverse=True)

        DraftPostFactory.create_batch(5)

        response = self.client.get('/')
        post = response.context['post']

        self.assertEqual(post, published_posts[0])

    def test_returns_upcoming_gigs(self):
        upcoming_gigs = UpcomingGigFactory.create_batch(5)
        upcoming_gigs = sorted(upcoming_gigs, key=lambda x: x.date)

        PastGigFactory.create_batch(5)
        DraftGigFactory.create_batch(5)

        response = self.client.get('/')
        gig_list = response.context['gig_list']

        self.assertEqual(list(gig_list), upcoming_gigs)
