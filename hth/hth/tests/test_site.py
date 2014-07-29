from time import sleep

from .base import SeleniumTestCase


class SiteTestCase(SeleniumTestCase):

    def test_can_access_site(self):
        self.get_url('')
        self.assertIn('Hallelujah The Hills', self.browser.title)

