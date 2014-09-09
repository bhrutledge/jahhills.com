from django.test import TestCase
from django.core.urlresolvers import reverse

from core.tests.utils import today_str
from ..models import Venue, Gig


class GigTestCase(TestCase):

    def setUp(self):
        today = today_str()
        tomorrow = today_str(1)
        yesterday = today_str(-1)

        today_venue = Venue.objects.create(name='Today', city='c')
        tomorrow_venue = Venue.objects.create(name='Tomorrow', city='c')
        yesterday_venue = Venue.objects.create(name='Yesterday', city='c')
        draft_venue = Venue.objects.create(name='Draft', city='c')

        self.today = Gig.objects.create(date=today, slug=today,
                                        venue=today_venue, publish=True)
        self.tomorrow = Gig.objects.create(date=tomorrow, slug=tomorrow,
                                           venue=tomorrow_venue,
                                           publish=True)
        self.yesterday = Gig.objects.create(date=yesterday, slug=yesterday,
                                            venue=yesterday_venue,
                                            publish=True)
        self.draft = Gig.objects.create(date=today, slug=today+'-d',
                                        venue=draft_venue)

    def test_list_name(self):
        self.assertEqual(reverse('gig_list'), '/shows/')

    def test_list_returns_published_gigs(self):
        response = self.client.get('/shows/')
        gig_list = response.context['gig_list']
        self.assertEqual(list(gig_list),
                         [self.tomorrow, self.today, self.yesterday])

    def test_list_uses_template(self):
        response = self.client.get('/shows/')
        self.assertTemplateUsed(response, 'shows/gig_list.html')

    def test_list_uses_one_query(self):
        with self.assertNumQueries(1):
            self.client.get('/shows/')
