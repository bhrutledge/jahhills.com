from django.test import TestCase
from django.core.urlresolvers import reverse

from hth.news.tests.factories import PostFactory, PublishedPostFactory
from hth.shows.tests.factories import (
    GigFactory, PastGigFactory, UpcomingGigFactory)
from hth.music.tests.factories import ReleaseFactory, PublishedReleaseFactory


class HomeTestCase(TestCase):

    def test_name(self):
        self.assertEqual(reverse('home_page'), '/')

    def test_uses_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home_page.html')

    def test_returns_latest_post(self):
        published_posts = PublishedPostFactory.create_batch(5)
        PostFactory.create_batch(5)

        response = self.client.get('/')
        post = response.context['post']

        self.assertEqual(post, published_posts[0])

    def test_returns_upcoming_gigs(self):
        upcoming_gigs = UpcomingGigFactory.create_batch(5)
        PastGigFactory.create_batch(5)
        GigFactory.create_batch(5)

        response = self.client.get('/')
        gig_list = response.context['gig_list']

        self.assertEqual(list(gig_list), upcoming_gigs)

    def test_returns_latest_release(self):
        published_releases = PublishedReleaseFactory.create_batch(5)
        ReleaseFactory.create_batch(5)

        response = self.client.get('/')
        release = response.context['release']

        self.assertEqual(release, published_releases[0])
