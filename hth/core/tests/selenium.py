from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


class SeleniumTestCase(StaticLiveServerCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    ## Convenience functions

    def get_url(self, url):
        return self.browser.get(self.live_server_url + url)

    def find_tag(self, tag_name):
        return self.browser.find_element_by_tag_name(tag_name)

    def find_name(self, name):
        return self.browser.find_element_by_name(name)

    def find_link(self, link_text):
        return self.browser.find_element_by_link_text(link_text)

    def find_css(self, css_selector):
        return self.browser.find_element_by_css_selector(css_selector)

    def find_select(self, name):
        return Select(self.find_name(name))


class AdminTestCase(SeleniumTestCase):

    # TODO: Create superuser programatically
    fixtures = ['core/admin.json']

    def adminLogin(self):
        self.get_url('/admin')
        self.assertIn('Log in', self.browser.title)

        self.find_name('username').send_keys('admin')
        self.find_name('password').send_keys('admin' + Keys.RETURN)

