from unittest import skip
from core.tests.selenium import SeleniumTestCase
from music.tests.factories import VideoFactory, PublishedVideoFactory


@skip('Out of sync with markup')
class VideosTestCase(SeleniumTestCase):

    def setUp(self):
        super().setUp()

        self.published_videos = PublishedVideoFactory.create_batch(10)
        VideoFactory.create_batch(5)

    def test_videos_detail_displays_entire_video(self):
        video = self.published_videos[0]

        self.get_url(video.get_absolute_url())

        self.assertEqual(self.find_css('.video .title')[0].text, video.title)
        self.assertEqual(video.description,
                         self.find_css('.video .description')[0].text)
        self.assertIn(video.credits,
                      self.find_css('.video .credits')[0].text)

    def test_videos_displays_published_video_titles(self):
        self.get_url('/video')
        self.assertIn('Videos', self.browser.title)

        displayed_titles = [x.text for x in self.find_css('.video .title')]
        published_titles = [x.title for x in self.published_videos]

        self.assertEqual(displayed_titles, published_titles)

    def test_home_displays_latest_video(self):
        self.get_url('')

        displayed_titles = [x.text for x in self.find_css('.video .title')]

        self.assertEqual(len(displayed_titles), 1)
        self.assertEqual(displayed_titles[0], self.published_videos[0].title)
