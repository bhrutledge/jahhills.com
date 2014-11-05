from core.tests.selenium import SeleniumTestCase
from music.tests.factories import (
    DraftReleaseFactory, PublishedReleaseFactory,
    DraftSongFactory, PublishedSongFactory)


class MusicTestCase(SeleniumTestCase):

    def setUp(self):
        super().setUp()

        self.published_releases = PublishedReleaseFactory.create_batch(10)
        DraftReleaseFactory.create_batch(5)

    def test_music_detail_displays_entire_release(self):
        release = self.published_releases[0]

        self.get_url(release.get_absolute_url())
        self.assertEqual(self.find_css('.release .title')[0].text,
                         release.title)
        self.assertEqual(self.find_css('.release .description p')[0].text,
                         release.description)
        self.assertEqual(self.find_css('.release .credits p')[0].text,
                         release.credits)

    # TODO: Tracks and videos

    def test_music_displays_published_releases(self):
        self.get_url('/music')
        self.assertIn('Music', self.browser.title)

        displayed_titles = [x.text for x in self.find_css('.release .title')]
        published_titles = [x.title for x in self.published_releases]

        displayed_descriptions = [x.text for x in
                                  self.find_css('.release .description p')]
        published_descriptions = [x.description for x in
                                  self.published_releases]

        self.assertEqual(displayed_titles, published_titles)
        self.assertEqual(displayed_descriptions, published_descriptions)

    def test_home_displays_latest_release(self):
        self.get_url('')

        displayed_titles = [x.text for x in self.find_css('.release .title')]
        displayed_descriptions = [x.text for x in
                                  self.find_css('.release .description p')]

        self.assertEqual(len(displayed_titles), 1)
        self.assertEqual(displayed_titles[0], self.published_releases[0].title)
        self.assertEqual(displayed_descriptions[0],
                         self.published_releases[0].description)


class SongsTestCase(SeleniumTestCase):

    def setUp(self):
        super().setUp()

        self.published_songs = PublishedSongFactory.create_batch(10)
        DraftSongFactory.create_batch(5)

    def test_song_detail_displays_entire_song(self):
        song = self.published_songs[0]

        self.get_url(song.get_absolute_url())
        self.assertEqual(self.find_css('.song .title')[0].text, song.title)
        self.assertEqual(self.find_css('.song .description p')[0].text,
                         song.description)
        self.assertEqual(self.find_css('.song .credits p')[0].text,
                         song.credits)
        self.assertEqual(self.find_css('.song .lyrics p')[0].text,
                         song.lyrics)

    def test_song_list_displays_published_songs(self):
        self.get_url('/songs')
        self.assertIn('Songs', self.browser.title)

        displayed_titles = [x.text for x in self.find_css('.song .title')]
        published_titles = [x.title for x in self.published_songs]

        self.assertEqual(displayed_titles, published_titles)
