from datetime import date, timedelta
from time import sleep

from .base import AdminTestCase


class PostTestCase(AdminTestCase):

    def test_can_create_post(self):
        # Ryan logs into the admin

        self.adminLogin()

        # TODO: He adds a draft News post

        # TODO: He previews the draft post on the site

        # He publishes a News post

        self.find_link('Posts').click()
        self.find_link('Add post').click()

        self.find_name('title').send_keys('First post')
        self.find_name('body').send_keys('Test content')
        self.find_name('_save').click()

        self.assertIn('First post', self.find_tag('body').text)

        # He verifies that it was published

        self.get_url('/news')
        self.find_link('First post').click()
        self.assertIn('First post', self.browser.title)

        # TODO: He schedules a post for the future

