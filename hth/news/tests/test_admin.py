from core.tests.selenium import AdminTestCase


class NewsTestCase(AdminTestCase):

    def test_can_create_post(self):
        # Ryan logs into the admin

        self.adminLogin()

        # He adds a draft Post

        self.find_link('Posts').click()
        self.find_link('Add post').click()

        self.find_name('title').send_keys('First post')
        self.find_name('body').send_keys('Test content')
        self.find_name('_save').click()
        self.assertIn('First post', self.find_tag('body').text)

        # TODO: He previews the draft post on the site

        # He makes sure that it's not published

        self.get_url('/news')
        self.assertIn('News', self.browser.title)
        self.assertNotIn('First post', self.find_tag('body').text)
        self.get_url('/news/first-post')
        self.assertNotIn('First post', self.browser.title)

        # He publishes the post

        self.get_url('/admin')
        self.find_link('Posts').click()
        self.find_link('First post').click()
        self.find_name('publish').click()
        self.find_name('_save').click()

        # He verifies that it was published

        self.get_url('/news')
        self.find_link('First post').click()
        self.assertIn('First post', self.browser.title)

        # TODO: He schedules a post for the future

        # TODO: He checks the order of the posts?
