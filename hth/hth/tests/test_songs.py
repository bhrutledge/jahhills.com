from time import sleep

from bandcms.tests.utils import today_str
from bandcms.models import Release
from .base import AdminTestCase


class SongTestCase(AdminTestCase):

    def setUp(self):
        super().setUp()
        Release(title='First release', slug='first-release',
                publish=True).save()

    def test_can_create_song(self):
        # Ryan logs into the admin

        self.adminLogin()

        # He adds a song to the release

        self.find_link('Songs').click()
        self.find_link('Add song').click()
        self.find_name('title').send_keys('First song')
        self.find_name('description').send_keys('Song description')
        self.find_name('credits').send_keys('Song credits')
        self.find_name('lyrics').send_keys('Song lyrics')
        self.find_name('publish').click()
        self.find_name('_save').click()

        self.assertIn('First song', self.find_tag('body').text)

        # He adds an unpublished song

        self.find_link('Add song').click()
        self.find_name('title').send_keys('Second song')
        self.find_name('_save').click()

        # He verifies that the published song is on the site

        self.get_url('/music/songs')
        self.assertNotIn('Second song', self.find_tag('body').text)
        self.find_link('First song').click()
        self.assertIn('First song', self.browser.title)

        # He adds the songs to the release

        self.get_url('/admin')
        self.find_link('Songs').click()
        self.find_link('First song').click()
        self.find_select('release').select_by_visible_text('first-release')
        self.find_name('track').send_keys('1')
        self.find_name('_save').click()

        self.find_link('Second song').click()
        self.find_select('release').select_by_visible_text('first-release')
        self.find_name('track').send_keys('2')
        self.find_name('_save').click()

        # He verifies that the published song is shown on the release

        self.get_url('/music/first-release')
        self.assertIn('First song', self.find_tag('body').text)
        self.assertNotIn('Second song', self.find_tag('body').text)

        self.find_link('First song').click()
        self.assertIn('First song', self.browser.title)

