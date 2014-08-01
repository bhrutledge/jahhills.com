from time import sleep

from bandcms.tests.utils import today_str
from .base import AdminTestCase


class ReleaseTestCase(AdminTestCase):

    def test_can_create_release(self):
        # Ryan logs into the admin

        self.adminLogin()

        # He adds a published release

        self.find_link('Releases').click()
        self.find_link('Add release').click()

        self.find_name('title').send_keys('First release')
        self.find_name('date').send_keys(today_str(1))
        self.find_name('description').send_keys('Release description')
        self.find_name('credits').send_keys('Release credits')
        self.find_name('_save').click()

        self.assertIn('First release', self.find_tag('body').text)

        # He verifies that it was published

        self.get_url('/music')
        self.find_link('First release').click()
        self.assertIn('First release', self.browser.title)

