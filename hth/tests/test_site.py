from time import sleep

from core.tests.selenium import SeleniumTestCase
from news.tests.factories import PostFactory
from news.models import Post

class SiteTestCase(SeleniumTestCase):

    def setUp(self):
        super().setUp()

        PostFactory.create_batch(10, publish=True)
        PostFactory.create_batch(5)

    def test_can_access_site(self):
        self.get_url('')
        self.assertIn('Hallelujah The Hills', self.browser.title)

        self.get_url('/admin')
        self.assertIn('Django site admin', self.browser.title)

        # TODO: Test against custom templates and fixtures

        self.get_url('/shows')
        self.assertIn('Shows', self.browser.title)

        self.get_url('/music')
        self.assertIn('Music', self.browser.title)

        self.get_url('/songs')
        self.assertIn('Songs', self.browser.title)

        self.get_url('/videos')
        self.assertIn('Videos', self.browser.title)

    def test_news_shows_all_published_posts(self):
        self.get_url('/news')
        self.assertIn('News', self.browser.title)

        live_titles = [p.text for p in self.find_css('.post .title')]
        published_titles = [p.title for p in Post.objects.published()]

        self.assertEqual(live_titles, published_titles)

    # def test_home_shows_most_recent_post(self):
    #     self.get_url('')
    #
    #     live_titles = [p.text for p in self.find_css('.post .title')]
    #     published_titles = [p.title for p in Post.objects.published()]
    #
    #     self.assertEqual(len(live_titles), 1)
    #     self.assertEqual(live_title[0], published_titles[0])
