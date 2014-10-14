from time import sleep

from django.template.defaultfilters import date as datefilter

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

    def test_news_detail_displays_entire_post(self):
        post = self.published_posts[0]

        post_text = '\n'.join([
            post.title, datefilter(post.publish_on), post.body])

        self.get_url(post.get_absolute_url())
        self.assertEqual(self.find_css('.post')[0].text, post_text)

    def test_news_displays_all_published_post_titles(self):
        self.get_url('/news')
        self.assertIn('News', self.browser.title)

        displayed_titles = [x.text for x in self.find_css('.post .title')]
        published_titles = [x.title for x in self.published_posts]

        self.assertEqual(displayed_titles, published_titles)

    def test_home_displays_latest_post(self):
        self.get_url('')

        displayed_titles = [x.text for x in self.find_css('.post .title')]

        self.assertEqual(len(displayed_titles), 1)
        self.assertEqual(displayed_titles[0], self.published_posts[0].title)
