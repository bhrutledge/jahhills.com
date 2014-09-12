from time import sleep

from core.tests.selenium import SeleniumTestCase
from news.tests.factories import DraftPostFactory, PublishedPostFactory


class NewsTestCase(SeleniumTestCase):

    def setUp(self):
        super().setUp()

        published_posts = PublishedPostFactory.create_batch(10)
        self.published_posts = sorted(published_posts,
                                      key=lambda x: x.publish_on,
                                      reverse=True)

        DraftPostFactory.create_batch(5)

    def test_news_displays_all_published_posts(self):
        self.get_url('/news')
        self.assertIn('News', self.browser.title)

        live_titles = [p.text for p in self.find_css('.post .title')]
        published_titles = [p.title for p in self.published_posts]

        self.assertEqual(live_titles, published_titles)

    def test_home_displays_latest_post(self):
        self.get_url('')

        post_list = self.find_css('.post')
        self.assertEqual(len(post_list), 1)

        latest_post = self.published_posts[0]

        post_title = self.find_css('.post .title')[0].text
        self.assertEqual(post_title, latest_post.title)
