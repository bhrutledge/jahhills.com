from core.tests.utils import date_format, from_today
from core.tests.selenium import AdminTestCase

from ..models import Venue


class VenueTestCase(AdminTestCase):

    def test_can_create_venue(self):
        # Ryan logs into the admin

        self.adminLogin()

        # He adds a venue

        self.find_link('Venues').click()
        self.find_link('ADD VENUE').click()

        self.find_name('name').send_keys('Great Scott')
        self.find_name('city').send_keys('Allston, MA')
        self.find_name('website').send_keys('http://greatscottboston.com')
        self.find_name('_save').click()
        self.assertIn('Great Scott', self.find_tag('body').text)


class GigTestCase(AdminTestCase):

    def setUp(self):
        super().setUp()

        self.venue1 = Venue.objects.create(
            name='Great Scott', city='Allston, MA')

        self.venue2 = Venue.objects.create(
            name='Middle East Upstairs', city='Cambridge, MA')

        self.venue3 = Venue.objects.create(
            name='Red Star Union', city='Cambridge, MA')

    def test_can_create_gig(self):
        # Ryan logs into the admin

        self.adminLogin()

        # He publishes an upcoming gig

        self.find_link('Gigs').click()
        self.find_link('ADD GIG').click()

        self.find_name('date').send_keys(date_format(from_today(1)))
        self.find_name('venue').send_keys(self.venue1.id)
        self.find_name('description').send_keys('with Tallahassee')
        self.find_name('details').send_keys('$5, 21+, Doors at 9pm')
        self.find_name('publish').click()
        self.find_name('_save').click()
        self.assertIn('Great Scott', self.find_tag('body').text)

        # He publishes a past gig

        self.find_link('ADD GIG').click()

        self.find_name('date').send_keys(date_format(from_today(-30)))
        self.find_name('venue').send_keys(self.venue2.id)
        self.find_name('description').send_keys('with Thick Wild')
        self.find_name('details').send_keys('$10, 18+, Doors at 8pm')
        self.find_name('publish').click()
        self.find_name('_save').click()
        self.assertIn('Middle East Upstairs', self.find_tag('body').text)

        # He drafts a future gig

        self.get_url('/admin')

        self.find_link('Gigs').click()
        self.find_link('ADD GIG').click()

        self.find_name('date').send_keys(date_format(from_today(30)))
        self.find_name('venue').send_keys(self.venue3.id)
        self.find_name('_save').click()
        self.assertIn('Red Star Union', self.find_tag('body').text)

        # He verifies that only the published gigs are visible

        self.get_url('/live')
        self.assertIn('Live', self.browser.title)
        self.assertIn('Great Scott', self.find_tag('body').text)
        self.assertIn('Middle East', self.find_tag('body').text)
        self.assertNotIn('Red Star Union', self.find_tag('body').text)
