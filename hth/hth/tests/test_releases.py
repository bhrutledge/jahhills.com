from time import sleep

from bandcms.tests.utils import today_str
from .base import AdminTestCase


class ReleaseTestCase(AdminTestCase):

    def test_can_create_release(self):
        # Ryan logs into the admin

        self.adminLogin()

        # He creates an unpublished release

        self.find_link('Releases').click()
        self.find_link('Add release').click()

        self.find_name('title').send_keys('First release')
        self.find_name('date').send_keys(today_str(1))
        self.find_name('description').send_keys('Release description')
        self.find_name('credits').send_keys('Release credits')
        self.find_name('_save').click()

        self.assertIn('First release', self.find_tag('body').text)

        # He verifies that it's not published

        self.get_url('/music')
        self.assertNotIn('First release', self.find_tag('body').text)
        self.get_url('/music/first-release')
        self.assertNotIn('First release', self.browser.title)

        # He publishes the release

        self.get_url('/admin')
        self.find_link('Releases').click()
        self.find_link('First release').click()
        self.find_name('publish').click()
        self.find_name('_save').click()

        # He verifies that it was published

        self.get_url('/music')
        self.find_link('First release').click()
        self.assertIn('First release', self.browser.title)

        # TODO: He adds album artwork
        # TODO: He adds songs
