from time import sleep

from django.template.defaultfilters import date as datefilter

from core.tests.selenium import SeleniumTestCase
from music.tests.factories import DraftReleaseFactory, PublishedReleaseFactory


class MusicTestCase(SeleniumTestCase):

    def setUp(self):
        super().setUp()

        published_releases = PublishedReleaseFactory.create_batch(10)
        self.published_releases = sorted(published_releases,
                                         key=lambda x: x.date,
                                         reverse=True)

        DraftReleaseFactory.create_batch(5)

    def test_music_detail_displays_entire_release(self):
        release = self.published_releases[0]

        self.get_url(release.get_absolute_url())
        self.assertEqual(self.find_css('.release .title')[0].text,
                         release.title)
        self.assertEqual(self.find_css('.release .description')[0].text,
                         release.description)

    # TODO: Tracks and videos

    def test_music_displays_published_releases(self):
        self.get_url('/music')
        self.assertIn('Music', self.browser.title)

        displayed_titles = [x.text for x in self.find_css('.release .title')]
        published_titles = [x.title for x in self.published_releases]

        self.assertEqual(displayed_titles, published_titles)

    def test_home_displays_latest_release(self):
        self.get_url('')

        displayed_titles = [x.text for x in self.find_css('.release .title')]

        self.assertEqual(len(displayed_titles), 1)
        self.assertEqual(displayed_titles[0], self.published_releases[0].title)
