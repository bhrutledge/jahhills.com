import vcr

from core.tests.utils import date_format, from_today
from core.tests.selenium import AdminTestCase

from .factories import PublishedReleaseFactory


class ReleaseTestCase(AdminTestCase):

    def test_can_create_release(self):
        # Ryan logs into the admin

        self.adminLogin()

        # He creates an unpublished release

        self.find_link('Releases').click()
        self.find_link('ADD RELEASE').click()

        self.find_name('title').send_keys('First release')
        self.find_name('date').send_keys(date_format(from_today(1)))
        self.find_name('cover_url').send_keys('http://localhost/cover.jpg')
        self.find_name('player_code').send_keys('<iframe></iframe>')
        self.find_name('description').send_keys('Release description')
        self.find_name('credits').send_keys('Release credits')
        self.find_name('_save').click()
        self.assertIn('First release', self.find_tag('body').text)

        # He verifies that it's not published

        self.get_url('/music')
        self.assertIn('Music', self.browser.title)
        self.assertNotIn('First release', self.find_tag('body').text)
        self.get_url('/music/first-release')
        self.assertNotIn('First release', self.browser.title)

        # He publishes the release

        self.get_url('/admin')
        self.find_link('Releases').click()
        self.find_link('First release').click()
        self.find_name('publish').click()
        self.find_name('_save').click()
        self.assertIn('First release', self.find_tag('body').text)

        # He verifies that it was published

        self.get_url('/music')
        self.find_link('First release').click()
        self.assertIn('First release', self.browser.title)

        # TODO: Test absence/presence of details?


class SongTestCase(AdminTestCase):

    def setUp(self):
        super().setUp()
        PublishedReleaseFactory.create(title='First release',
                                       slug='first-release')

    def test_can_create_song(self):
        # Ryan logs into the admin

        self.adminLogin()

        # He adds a published song

        self.find_link('Songs').click()
        self.find_link('ADD SONG').click()
        self.find_name('title').send_keys('First song')
        self.find_name('description').send_keys('Song description')
        self.find_name('player_code').send_keys('<iframe></iframe>')
        self.find_name('credits').send_keys('Song credits')
        self.find_name('lyrics').send_keys('Song lyrics')
        self.find_name('publish').click()
        self.find_name('_save').click()
        self.assertIn('First song', self.find_tag('body').text)

        # He adds an unpublished song

        self.find_link('ADD SONG').click()
        self.find_name('title').send_keys('Second song')
        self.find_name('_save').click()
        self.assertIn('Second song', self.find_tag('body').text)

        # He verifies that only the published song is on the site

        self.get_url('/songs')
        self.assertIn('Songs', self.browser.title)
        self.assertNotIn('Second song', self.find_tag('body').text)
        self.find_link('First song').click()
        self.assertIn('First song', self.browser.title)

        # He adds the songs to the release

        self.get_url('/admin')
        self.find_link('Songs').click()
        self.find_link('First song').click()
        self.find_select('release').select_by_visible_text('First release')
        self.find_name('track').send_keys('1')
        self.find_name('_save').click()

        self.find_link('Second song').click()
        self.find_select('release').select_by_visible_text('First release')
        self.find_name('track').send_keys('2')
        self.find_name('_save').click()

        # He verifies that only the published song is shown on the release

        self.get_url('/music/first-release')
        self.assertIn('First song', self.find_tag('body').text)
        self.assertNotIn('Second song', self.find_tag('body').text)


class VideoTestCase(AdminTestCase):

    # TODO: Duplicated in .test_models.VideoAutofillTestCase
    CASSETTE = 'music/tests/fixtures/cassettes/vimeo.yaml'
    SOURCE_URL = 'https://vimeo.com/126794989'
    PREVIEW_URL = 'http://i.vimeocdn.com/video/517362144_640.jpg'
    EMBED_CODE = ('<iframe src="http://player.vimeo.com/video/126794989"'
                  ' seamless allowfullscreen></iframe>\n')

    def setUp(self):
        super().setUp()
        PublishedReleaseFactory.create(title='First release',
                                       slug='first-release')

    def test_can_create_video(self):
        # Ryan logs into the admin

        self.adminLogin()

        # He adds a published video

        self.find_link('Videos').click()
        self.find_link('ADD VIDEO').click()
        self.find_name('title').send_keys('First video')
        self.find_name('source_url').send_keys('http://localhost')
        self.find_name('embed_code').send_keys('<iframe></iframe>')
        self.find_name('preview_url').send_keys('http://localhost/jpg')
        self.find_name('description').send_keys('Video description')
        self.find_name('credits').send_keys('Video credits')
        self.find_name('publish').click()
        self.find_name('_save').click()
        self.assertIn('First video', self.find_tag('body').text)

        # He adds an unpublished video

        self.find_link('ADD VIDEO').click()
        self.find_name('title').send_keys('Second video')
        self.find_name('_save').click()
        self.assertIn('Second video', self.find_tag('body').text)

        # He verifies that only the published video is on the site

        self.get_url('/video')
        self.assertNotIn('Second video', self.find_tag('body').text)
        self.find_link('First video').click()
        self.assertIn('First video', self.browser.title)

        # He adds the videos to the release

        self.get_url('/admin')
        self.find_link('Videos').click()
        self.find_link('First video').click()
        self.find_select('release').select_by_visible_text('First release')
        self.find_name('_save').click()

        self.find_link('Second video').click()
        self.find_select('release').select_by_visible_text('First release')
        self.find_name('_save').click()

        # He verifies that only the published video is shown on the release

        self.get_url('/music/first-release')
        self.assertIn('First video', self.find_tag('body').text)
        self.assertNotIn('Second video', self.find_tag('body').text)

        self.find_link('First video').click()
        self.assertIn('First video', self.browser.title)

    @vcr.use_cassette(CASSETTE)
    def test_autofill_from_source(self):
        # Ryan logs into the admin

        self.adminLogin()

        # He adds a published video, without preview_url and embed_code

        self.find_link('Videos').click()
        self.find_link('ADD VIDEO').click()
        self.find_name('title').send_keys('First video')
        self.find_name('source_url').send_keys(self.SOURCE_URL)
        self.find_name('publish').click()
        self.find_name('_continue').click()

        # He verifies that the preview_url and embed_code have been filled

        self.assertEqual(self.PREVIEW_URL,
                         self.find_name('preview_url').get_attribute('value'))
        self.assertEqual(self.EMBED_CODE.strip(),
                         self.find_name('embed_code').text)

        # He verifies that the published video is on the site

        self.get_url('/video')
        self.find_link('First video').click()
        self.assertIn('First video', self.browser.title)


class PressTestCase(AdminTestCase):

    def setUp(self):
        super().setUp()
        PublishedReleaseFactory.create(title='First release',
                                       slug='first-release')

    def test_can_create_quote(self):
        # Ryan logs into the admin

        self.adminLogin()

        # He adds a published quote

        self.find_link('Press').click()
        self.find_link('ADD PRESS').click()
        self.find_name('title').send_keys('First source')
        self.find_name('source_url').send_keys('http://example.com')
        self.find_name('date').send_keys(date_format(from_today(-30)))
        self.find_name('body').send_keys('First quote')
        self.find_name('publish').click()
        self.find_name('_save').click()
        self.assertIn('First source', self.find_tag('body').text)

        # He adds an unpublished quote

        self.find_link('ADD PRESS').click()
        self.find_name('title').send_keys('Second source')
        self.find_name('source_url').send_keys('http://foo.com')
        self.find_name('date').send_keys(date_format(from_today(-30)))
        self.find_name('_save').click()
        self.assertIn('Second source', self.find_tag('body').text)

        # He verifies that only the published quote is on the site

        self.get_url('/press')
        self.assertIn('Press', self.browser.title)
        self.assertIn('First source', self.find_tag('body').text)
        self.assertIn('First quote', self.find_tag('body').text)
        self.assertNotIn('Second source', self.find_tag('body').text)
        self.assertNotIn('Second quote', self.find_tag('body').text)

        # He adds the quotes to the release

        self.get_url('/admin')
        self.find_link('Press').click()
        self.find_link('First source').click()
        self.find_select('release').select_by_visible_text('First release')
        self.find_name('_save').click()

        self.find_link('Second source').click()
        self.find_select('release').select_by_visible_text('First release')
        self.find_name('_save').click()

        # He verifies that only the published quote is shown on the release

        self.get_url('/music/first-release')
        self.assertIn('First source', self.find_tag('body').text)
        self.assertNotIn('Second source', self.find_tag('body').text)

    def test_can_create_post(self):
        # Ryan logs into the admin

        self.adminLogin()

        # He adds a published press post

        self.find_link('Press').click()
        self.find_link('ADD PRESS').click()
        self.find_name('title').send_keys('Post title')
        self.find_name('body').send_keys('Post body')
        self.find_name('date').send_keys(date_format(from_today(-30)))
        self.find_name('quote').click()
        self.find_name('publish').click()
        self.find_name('_save').click()
        self.assertIn('Post title', self.find_tag('body').text)

        # He verifies that the post is on the site

        self.get_url('/press')
        self.assertIn('Press', self.browser.title)
        self.assertIn('Post title', self.find_tag('body').text)
        self.assertIn('Post body', self.find_tag('body').text)

        # He adds the post to the release

        self.get_url('/admin')
        self.find_link('Press').click()
        self.find_link('Post title').click()
        self.find_select('release').select_by_visible_text('First release')
        self.find_name('_save').click()

        # He verifies that post is shown on the release

        self.get_url('/music/first-release')
        self.assertIn('Post title', self.find_tag('body').text)
