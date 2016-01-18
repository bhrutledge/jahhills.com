from django.template.defaultfilters import date as datefilter

from core.tests.selenium import SeleniumTestCase
from shows.tests.factories import (
    DraftGigFactory, PastGigFactory, UpcomingGigFactory)


class ShowsTestCase(SeleniumTestCase):

    def setUp(self):
        super().setUp()

        self.upcoming_gigs = UpcomingGigFactory.create_batch(10)
        self.past_gigs = PastGigFactory.create_batch(10)
        DraftGigFactory.create_batch(5)

    def test_shows_displays_upcoming_gigs_before_past_gigs(self):
        self.get_url('/shows')
        self.assertIn('Shows', self.browser.title)

        from time import sleep
        sleep(10)

        displayed_dates = [x.text for x in self.find_css('.gig .date')]
        upcoming_dates = [datefilter(x.date) for x in self.upcoming_gigs]
        past_dates = [datefilter(x.date) for x in self.past_gigs]

        displayed_descriptions = [x.text for x in
                                  self.find_css('.gig .description')]
        upcoming_descriptions = [x.description for x in self.upcoming_gigs]
        past_descriptions = [x.description for x in self.past_gigs]

        self.assertEqual(displayed_dates, upcoming_dates + past_dates)
        self.assertEqual(displayed_descriptions,
                         upcoming_descriptions + past_descriptions)

    def test_shows_displays_details_for_upcoming_gigs(self):
        self.get_url('/shows')

        displayed_details = [x.text for x in self.find_css('.gig .details')]
        upcoming_details = [x.details for x in self.upcoming_gigs]

        self.assertEqual(displayed_details, upcoming_details)

    def test_home_displays_upcoming_gigs(self):
        self.get_url('')

        displayed_dates = [x.text for x in self.find_css('.gig .date')]
        upcoming_dates = [datefilter(x.date) for x in self.upcoming_gigs]

        displayed_descriptions = [x.text for x in
                                  self.find_css('.gig .description')]
        upcoming_descriptions = [x.description for x in self.upcoming_gigs]

        displayed_details = [x.text for x in self.find_css('.gig .details')]
        upcoming_details = [x.details for x in self.upcoming_gigs]

        self.assertEqual(displayed_dates, upcoming_dates)
        self.assertEqual(displayed_descriptions, upcoming_descriptions)
        self.assertEqual(displayed_details, upcoming_details)
