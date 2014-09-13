from time import sleep

from django.template.defaultfilters import date as datefilter

from core.tests.selenium import SeleniumTestCase
from shows.tests.factories import (
    DraftGigFactory, PastGigFactory, UpcomingGigFactory)


class ShowsTestCase(SeleniumTestCase):

    def setUp(self):
        super().setUp()

        upcoming_gigs = UpcomingGigFactory.create_batch(10)
        self.upcoming_gigs = sorted(upcoming_gigs, key=lambda x: x.date)

        past_gigs = PastGigFactory.create_batch(10)
        self.past_gigs = sorted(past_gigs, key=lambda x: x.date, reverse=True)

        DraftGigFactory.create_batch(5)

    def test_shows_displays_upcoming_gigs_before_past_gigs(self):
        self.get_url('/shows')
        self.assertIn('Shows', self.browser.title)

        displayed_dates = [g.text for g in self.find_css('.gig .date')]
        upcoming_dates = [datefilter(g.date) for g in self.upcoming_gigs]
        past_dates = [datefilter(g.date) for g in self.past_gigs]

        self.assertEqual(displayed_dates, upcoming_dates + past_dates)

    def test_shows_displays_details_for_upcoming_gigs(self):
        self.get_url('/shows')

        displayed_details = [g.text for g in self.find_css('.gig .details')]
        upcoming_details = [g.details for g in self.upcoming_gigs]

        self.assertEqual(displayed_details, upcoming_details)

    # TODO: Find a better way to test use of select_related
    def test_shows_efficiently_displays_venue(self):
        with self.assertNumQueries(2):
            self.get_url('/shows')

            displayed_venues = [g.text for
                                g in self.find_css('.gig .venue')]
            expected_venues = [g.venue.name for
                               g in self.upcoming_gigs + self.past_gigs]

            self.assertEqual(displayed_venues, expected_venues)
