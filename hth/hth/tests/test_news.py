from time import sleep

from core.tests.selenium import SeleniumTestCase
from news.tests.factories import DraftPostFactory, PublishedPostFactory
from news.models import Post


class NewsTestCase(SeleniumTestCase):

    def setUp(self):
        super().setUp()

        PublishedPostFactory.create_batch(10)
        DraftPostFactory.create_batch(5)

    def test_news_displays_all_published_posts(self):
        self.get_url('/news')
        self.assertIn('News', self.browser.title)

        live_titles = [p.text for p in self.find_css('.post .title')]
        published_titles = [p.title for p in Post.objects.published()]

        self.assertEqual(live_titles, published_titles)

    def test_home_displays_most_recent_post(self):
        self.get_url('')

        post_list = self.find_css('.post')
        self.assertEqual(len(post_list), 1)

        last_post = Post.objects.published()[0]

        post_title = self.find_css('.post .title')[0].text
        self.assertEqual(post_title, last_post.title)

        post_body = self.find_css('.post .body')[0].text
        self.assertEqual(post_body, last_post.body)
