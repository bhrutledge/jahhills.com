from time import sleep

from bandcms.test_live.base import SeleniumTestCase


class SiteTestCase(SeleniumTestCase):

    def test_can_access_site(self):
        self.get_url('')
        self.assertIn('Hallelujah The Hills', self.browser.title)

        self.get_url('/admin')
        self.assertIn('Django site admin', self.browser.title)

        # TODO: Test against custom templates and fixtures

        self.get_url('/news')
        self.assertIn('Posts', self.browser.title)

        self.get_url('/calendar')
        self.assertIn('Gigs', self.browser.title)

        self.get_url('/music')
        self.assertIn('Releases', self.browser.title)

        self.get_url('/music/songs')
        self.assertIn('Songs', self.browser.title)

        self.get_url('/videos')
        self.assertIn('Videos', self.browser.title)

