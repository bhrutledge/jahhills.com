from django.test import override_settings
from time import sleep

from bandcms.models import Release
from .base import AdminTestCase


@override_settings(ROOT_URLCONF='bandcms.tests.live.urls')
class VideoTestCase(AdminTestCase):

    def setUp(self):
        super().setUp()
        Release(title='First release', slug='first-release',
                publish=True).save()

    def test_can_create_video(self):
        # Ryan logs into the admin

        self.adminLogin()

        # He adds a published video 

        self.find_link('Videos').click()
        self.find_link('Add video').click()
        self.find_name('title').send_keys('First video')
        self.find_name('source_url').send_keys('http://youtube.com')
        self.find_name('embed_code').send_keys('<iframe></iframe>')
        self.find_name('description').send_keys('Video description')
        self.find_name('credits').send_keys('Video credits')
        self.find_name('publish').click()
        self.find_name('_save').click()

        self.assertIn('First video', self.find_tag('body').text)

        # He adds an unpublished video

        self.find_link('Add video').click()
        self.find_name('title').send_keys('Second video')
        self.find_name('_save').click()

        # He verifies that the published video is on the site

        self.get_url('/videos')
        self.assertNotIn('Second video', self.find_tag('body').text)
        self.find_link('First video').click()
        self.assertIn('First video', self.browser.title)

        # He adds the videos to the release

        self.get_url('/admin')
        self.find_link('Videos').click()
        self.find_link('First video').click()
        self.find_select('release').select_by_visible_text('first-release')
        self.find_name('_save').click()

        self.find_link('Second video').click()
        self.find_select('release').select_by_visible_text('first-release')
        self.find_name('_save').click()

        # He verifies that the published video is shown on the release

        self.get_url('/releases/first-release')
        self.assertIn('First video', self.find_tag('body').text)
        self.assertNotIn('Second video', self.find_tag('body').text)

        self.find_link('First video').click()
        self.assertIn('First video', self.browser.title)

