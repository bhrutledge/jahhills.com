from datetime import datetime

from django.test import TestCase, override_settings
from django.core.urlresolvers import reverse

from bandcms.tests.utils import today_str
from ..models import AbstractCmsModel, Gig


class ModelTestCase(TestCase):

    def test_gig_is_cms_model(self):
        self.assertTrue(issubclass(Gig, AbstractCmsModel))

    def test_can_save_gig(self):
        g = Gig(date='2014-07-24', slug='2014-07-24',
                venue='Venue', city='City')
        g.full_clean()
        g.save()

        Gig.objects.get(slug='2014-07-24')

    def test_gig_can_have_details(self):
        g = Gig(date='2014-07-24', slug='2014-07-24',
                venue='Venue', city='City',
                description='Description', details='Details')
        g.full_clean()
        g.save()

    def test_gigs_ordered_by_date(self):

        g1 = Gig(date='2014-07-26', slug='2014-07-26',
                 venue='Venue', city='City')
        g2 = Gig(date='2014-07-25', slug='2014-07-25',
                 venue='Venue', city='City')
        g3 = Gig(date='2014-07-24', slug='2014-07-24',
                 venue='Venue', city='City')

        g2.save()
        g1.save()
        g3.save()

        self.assertEqual(list(Gig.objects.all()), [g1, g2, g3])


@override_settings(ROOT_URLCONF='bandcms.urls.gigs')
class UrlTestCase(TestCase):

    def setUp(self):
        today = today_str()
        tomorrow = today_str(1)
        yesterday = today_str(-1)

        Gig(date=today, slug=today, venue='Today', city='c').save()
        Gig(date=tomorrow, slug=tomorrow, venue='Tomorrow', city='c').save()
        Gig(date=yesterday, slug=yesterday, venue='Yesterday', city='c').save()
        Gig(date=today, slug=today+'-d', venue='Draft', city='c',
            publish=False).save()

    def test_list_shows_published_gigs(self):
        response = self.client.get(reverse('gig_list'))
        self.assertTemplateUsed(response, 'bandcms/gig_list.html')

        self.assertContains(response, 'Today')
        self.assertContains(response, 'Tomorrow')
        self.assertContains(response, 'Yesterday')
        self.assertNotContains(response, 'Draft')

