from django.test import TestCase


class UrlTestCase(TestCase):

    def test_home_page(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home_page.html')

