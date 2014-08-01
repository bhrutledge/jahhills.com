from time import sleep

from bandcms.tests.utils import today_str
from .base import AdminTestCase


class GigTestCase(AdminTestCase):

    def test_can_create_gig(self):
        # Ryan logs into the admin

        self.adminLogin()

        # He adds an upcoming gig

        self.find_link('Gigs').click()
        self.find_link('Add gig').click()

        self.find_name('date').send_keys(today_str(1))
        self.find_name('venue').send_keys('Great Scott')
        self.find_name('city').send_keys('Allston, MA')
        self.find_name('description').send_keys('with Tallahassee')
        self.find_name('details').send_keys('$5, 21+, Doors at 9pm')
        self.find_name('_save').click()

        # He adds a past gig

        self.find_link('Add gig').click()

        self.find_name('date').send_keys(today_str(-30))
        self.find_name('venue').send_keys('Middle East Upstairs')
        self.find_name('city').send_keys('Cambridge, MA')
        self.find_name('description').send_keys('with Thick Wild')
        self.find_name('details').send_keys('$10, 18+, Doors at 8pm')
        self.find_name('_save').click()

        # TODO: He publishes the gigs

        # He verifies that they were published

        self.get_url('/calendar')
        self.assertIn('Great Scott', self.find_tag('body').text)
        self.assertIn('Middle East', self.find_tag('body').text)

