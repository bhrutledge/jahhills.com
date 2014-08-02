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
        from bandcms.models import Release

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

        # TODO: He adds an unpublished song

        # TODO: He verifies that the published song is on the site

        # TODO: He adds the songs to the release

        #self.find_select('release').select_by_value('first-release')
        #self.find_name('track').send_keys('1')

