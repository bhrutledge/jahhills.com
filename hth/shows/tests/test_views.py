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

        Gig(date=today, slug=today, venue=today_venue,
            publish=True).save()
        Gig(date=tomorrow, slug=tomorrow, venue=tomorrow_venue,
            publish=True).save()
        Gig(date=yesterday, slug=yesterday, venue=yesterday_venue,
            publish=True).save()
        Gig(date=today, slug=today+'-d', venue=draft_venue).save()

    def test_list_name(self):
        self.assertEqual(reverse('gig_list'), '/shows/')

    def test_list_shows_published_gigs(self):
        response = self.client.get('/shows/')
        self.assertTemplateUsed(response, 'shows/gig_list.html')

        self.assertContains(response, 'Today')
        self.assertContains(response, 'Tomorrow')
        self.assertContains(response, 'Yesterday')
        self.assertNotContains(response, 'Draft')

