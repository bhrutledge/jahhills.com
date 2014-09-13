from django.test import TestCase
from django.core.urlresolvers import reverse

from .factories import DraftGigFactory, UpcomingGigFactory, PastGigFactory


class GigTestCase(TestCase):

    def setUp(self):
        self.draft_gigs = DraftGigFactory.create_batch(5)
        self.upcoming_gigs = UpcomingGigFactory.create_batch(5)
        self.past_gigs = PastGigFactory.create_batch(5)

    def test_list_name(self):
        self.assertEqual(reverse('gig_list'), '/shows/')

    def test_list_returns_published_gigs(self):
        published_gigs = sorted(self.upcoming_gigs + self.past_gigs,
                                key=lambda x: x.date,
                                reverse=True)

        response = self.client.get('/shows/')
        gig_list = response.context['gig_list']

        self.assertEqual(list(gig_list), published_gigs)

    def test_list_uses_template(self):
        response = self.client.get('/shows/')
        self.assertTemplateUsed(response, 'shows/gig_list.html')

    def test_list_uses_one_query(self):
        with self.assertNumQueries(1):
            self.client.get('/shows/')
