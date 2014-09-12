from time import sleep

from django.template.defaultfilters import date as datefilter

from core.tests.selenium import SeleniumTestCase
from shows.tests.factories import (
    DraftGigFactory, PastGigFactory, UpcomingGigFactory)


class ShowsTestCase(SeleniumTestCase):

    def setUp(self):
        super().setUp()

        upcoming_gigs = UpcomingGigFactory.create_batch(10)
        self.upcoming_gigs = sorted(upcoming_gigs, key=lambda x: x.date,
                                    reverse=True)

        past_gigs = PastGigFactory.create_batch(10)
        self.past_gigs = sorted(past_gigs, key=lambda x: x.date, reverse=True)

        DraftGigFactory.create_batch(5)

    def test_shows_displays_all_gigs(self):
        # TODO: def test_shows_displays_upcoming_gigs_before_past_gigs(self):
        self.get_url('/shows')
        self.assertIn('Shows', self.browser.title)

        displayed_dates = [g.text for g in self.find_css('.gig .date')]
        upcoming_dates = [datefilter(g.date) for g in self.upcoming_gigs]
        past_dates = [datefilter(g.date) for g in self.past_gigs]

        self.assertEqual(displayed_dates, upcoming_dates + past_dates)

    # def test_home_displays_upcoming_gigs(self):
    #     self.get_url('')
    #
    #     gig_list = self.find_css('.gig')
