from datetime import datetime

from django.test import TestCase
from django.utils import timezone
import vcr

from core.tests.models import (
    FieldsTestMixin, PublishTestMixin, TitleTestMixin)

from ..models import Release, Song, Video, Press
from .factories import (ReleaseFactory, PublishedReleaseFactory,
                        SongFactory, PublishedSongFactory,
                        VideoFactory, PublishedVideoFactory,
                        PressFactory, PublishedPressFactory)


class ReleaseTestCase(FieldsTestMixin, PublishTestMixin, TitleTestMixin,
                      TestCase):

    model = Release
    factory = ReleaseFactory
    required_fields = ['title', 'slug']

    def test_ordered_by_date(self):
        second = ReleaseFactory.create(date='2014-08-01')
        third = ReleaseFactory.create(date='2014-07-31')
        first = ReleaseFactory.create(date='2014-08-31')

        self.assertEqual(list(Release.objects.all()), [first, second, third])

    def test_ordered_by_priority(self):
        third = ReleaseFactory.create(date='2014-08-01', priority=1)
        first = ReleaseFactory.create(date='2014-07-31', priority=10)
        fourth = ReleaseFactory.create(date='2014-07-01')
        second = ReleaseFactory.create(date='2014-08-31', priority=1)

        self.assertEqual(list(Release.objects.all()),
                         [first, second, third, fourth])


class SongTestCase(FieldsTestMixin, PublishTestMixin, TitleTestMixin,
                   TestCase):

    model = Song
    factory = SongFactory
    required_fields = ['title', 'slug']

    def test_ordered_by_title(self):
        second = SongFactory.create(title='Second')
        first = SongFactory.create(title='First')
        third = SongFactory.create(title='Third')

        self.assertEqual(list(Song.objects.all()), [first, second, third])

    def test_tracks_can_be_added_to_release(self):
        r = PublishedReleaseFactory.create()

        publish = PublishedSongFactory.create(release=r, track=1)
        draft = SongFactory.create(release=r, track=2)

        tracks = list(r.tracks.all())
        self.assertIn(publish, tracks)
        self.assertNotIn(draft, tracks)

    def test_tracks_ordered_by_number(self):
        r = PublishedReleaseFactory.create()

        # Save out of order to test ordering
        s3 = PublishedSongFactory.create(release=r, track=3)
        s1 = PublishedSongFactory.create(release=r, track=1)
        s2 = PublishedSongFactory.create(release=r, track=2)

        self.assertEqual(list(r.tracks.all()), [s1, s2, s3])

    def test_release_has_lyrics(self):
        r = PublishedReleaseFactory.create()
        self.assertFalse(r.has_lyrics)

        PublishedSongFactory.create(release=r, track=1, lyrics='')
        self.assertFalse(r.has_lyrics)

        PublishedSongFactory.create(release=r, track=2, lyrics='lyrics')
        self.assertTrue(r.has_lyrics)

    def test_has_details(self):
        self.assertFalse(Song().has_details)
        self.assertTrue(Song(player_code='p').has_details)
        self.assertTrue(Song(description='d').has_details)
        self.assertTrue(Song(credits='c').has_details)
        self.assertTrue(Song(lyrics='l').has_details)
        self.assertTrue(SongFactory.create().has_details)


class VideoTestCase(FieldsTestMixin, PublishTestMixin, TitleTestMixin,
                    TestCase):

    model = Video
    factory = VideoFactory
    required_fields = ['title', 'slug']

    def test_ordered_by_date(self):
        draft = VideoFactory.create()

        first = PublishedVideoFactory.create(
            publish_on=datetime(2014, 7, 22, tzinfo=timezone.utc))

        old = PublishedVideoFactory.create(
            publish_on=datetime(2014, 7, 21, tzinfo=timezone.utc))

        new = PublishedVideoFactory.create(
            publish_on=datetime(2014, 7, 23, tzinfo=timezone.utc))

        self.assertEqual(list(Video.objects.all()), [draft, new, first, old])

    def test_can_be_added_to_release(self):
        r = PublishedReleaseFactory.create()

        publish = PublishedVideoFactory.create(release=r)
        draft = VideoFactory.create(release=r)

        videos = list(r.videos.all())
        self.assertIn(publish, videos)
        self.assertNotIn(draft, videos)

    def test_release_videos_ordered_by_date(self):
        r = PublishedReleaseFactory.create()

        # Save out of order to test ordering
        first = PublishedVideoFactory.create(
            publish_on=datetime(2014, 8, 1, tzinfo=timezone.utc),
            release=r)
        old = PublishedVideoFactory.create(
            publish_on=datetime(2014, 7, 31, tzinfo=timezone.utc),
            release=r)
        new = PublishedVideoFactory.create(
            publish_on=datetime(2014, 8, 31, tzinfo=timezone.utc),
            release=r)

        self.assertEqual(list(r.videos.all()), [new, first, old])


class VideoAutofillTestCase(TestCase):

    # TODO: Duplicated .test_admin.VideoTestCase
    CASSETTE = 'music/tests/fixtures/cassettes/vimeo.yaml'
    SOURCE_URL = 'https://vimeo.com/126794989'
    PREVIEW_URL = 'https://i.vimeocdn.com/video/517362144_640.jpg'
    EMBED_CODE = ('<iframe src="https://player.vimeo.com/video/126794989"'
                  ' seamless allowfullscreen></iframe>\n')

    @vcr.use_cassette(CASSETTE)
    def test_autofill_preview_url(self):
        embed_code = '<iframe></iframe>'

        VideoFactory.create(source_url=self.SOURCE_URL,
                            embed_code=embed_code)

        v = Video.objects.first()
        self.assertEqual(v.preview_url, self.PREVIEW_URL)
        self.assertEqual(v.embed_code, embed_code)

    @vcr.use_cassette(CASSETTE)
    def test_autofill_embed_code(self):
        preview_url = 'http://localhost/jpg'
        VideoFactory.create(source_url=self.SOURCE_URL,
                            preview_url=preview_url)

        v = Video.objects.first()
        self.assertEqual(v.preview_url, preview_url)
        self.assertEqual(v.embed_code, self.EMBED_CODE)

    @vcr.use_cassette(CASSETTE)
    def test_autofill_preview_url_and_embed_code(self):
        VideoFactory.create(source_url=self.SOURCE_URL)

        v = Video.objects.first()
        self.assertEqual(v.preview_url, self.PREVIEW_URL)
        self.assertEqual(v.embed_code, self.EMBED_CODE)

    def test_no_error_on_missing_source(self):
        VideoFactory.create()

        v = Video.objects.first()
        self.assertEqual(v.preview_url, '')
        self.assertEqual(v.embed_code, '')

    def test_no_error_on_unknown_source(self):
        VideoFactory.create(source_url='http://localhost')

        v = Video.objects.first()
        self.assertEqual(v.preview_url, '')
        self.assertEqual(v.embed_code, '')


class PressTestCase(FieldsTestMixin, PublishTestMixin, TestCase):

    model = Press
    factory = PressFactory
    required_fields = ['title', 'date']

    def test_quote_by_default(self):
        p = self.factory.create()
        self.assertTrue(p.quote)

    def test_str_is_title_and_date(self):
        p = PressFactory.build(title='Source', date='2014-07-25')
        self.assertEqual(str(p), 'Source, 2014-07-25')

    def test_ordered_by_date(self):
        # Save out of order to test ordering
        first = PressFactory.create(date='2014-08-01')
        old = PressFactory.create(date='2014-07-31')
        new = PressFactory.create(date='2014-08-31')

        self.assertEqual(list(Press.objects.all()), [new, first, old])

    def test_can_be_added_to_release(self):
        r = PublishedReleaseFactory.create()

        publish = PublishedPressFactory.create(release=r)
        draft = PressFactory.create(release=r)

        press = list(r.press.all())
        self.assertIn(publish, press)
        self.assertNotIn(draft, press)

    def test_release_press_ordered_by_date(self):
        r = PublishedReleaseFactory.create()

        # Save out of order to test ordering
        first = PublishedPressFactory.create(date='2014-08-01', release=r)
        old = PublishedPressFactory.create(date='2014-07-31', release=r)
        new = PublishedPressFactory.create(date='2014-08-31', release=r)

        self.assertEqual(list(r.press.all()), [new, first, old])
