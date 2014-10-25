from core.tests.selenium import SeleniumTestCase


class SiteTestCase(SeleniumTestCase):

    def test_can_access_site(self):
        self.get_url('')
        self.assertIn('Hallelujah The Hills', self.browser.title)

        self.get_url('/admin')
        self.assertIn('Django site admin', self.browser.title)
