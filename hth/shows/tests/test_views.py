from django.test import TestCase
from django.core.urlresolvers import reverse

from core.tests.utils import today_str
from ..models import Gig


class GigTestCase(TestCase):

    def setUp(self):
        today = today_str()
        tomorrow = today_str(1)
        yesterday = today_str(-1)

        Gig(date=today, slug=today, venue='Today', city='c',
            publish=True).save()
        Gig(date=tomorrow, slug=tomorrow, venue='Tomorrow', city='c',
            publish=True).save()
        Gig(date=yesterday, slug=yesterday, venue='Yesterday', city='c',
            publish=True).save()
        Gig(date=today, slug=today+'-d', venue='Draft', city='c').save()

    def test_list_name(self):
        self.assertEqual(reverse('gig_list'), '/shows/')

    def test_list_shows_published_gigs(self):
        response = self.client.get('/shows/')
        self.assertTemplateUsed(response, 'shows/gig_list.html')

        self.assertContains(response, 'Today')
        self.assertContains(response, 'Tomorrow')
        self.assertContains(response, 'Yesterday')
        self.assertNotContains(response, 'Draft')

