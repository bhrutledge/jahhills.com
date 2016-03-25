from django.test import TestCase
from django.core.urlresolvers import reverse

from ..models import Release, Song, Video
from .factories import (
    PublishedReleaseFactory, SongFactory, PublishedSongFactory,
    PressFactory, PublishedPressFactory,
)


class ReleaseTestCase(TestCase):

    def setUp(self):
        self.publish = Release.objects.create(
            title='Publish', slug='publish', publish=True)

        self.draft = Release.objects.create(title='Draft', slug='draft')

    def test_url_uses_slug(self):
        self.assertEqual(self.publish.get_absolute_url(), '/music/publish/')

    def test_can_view_published_releases(self):
        response = self.client.get('/music/publish/')
        release = response.context['release']
        self.assertEquals(self.publish, release)

    def test_detail_uses_template(self):
        response = self.client.get('/music/publish/')
        self.assertTemplateUsed(response, 'music/release_detail.html')

    def test_cant_view_draft_releases(self):
        response = self.client.get('/music/draft/')
        self.assertEqual(response.status_code, 404)

    def test_list_returns_published_releases(self):
        response = self.client.get('/music/')
        release_list = response.context['release_list']
        self.assertIn(self.publish, release_list)
        self.assertNotIn(self.draft, release_list)

    def test_list_uses_template(self):
        response = self.client.get('/music/')
        self.assertTemplateUsed(response, 'music/release_list.html')


class SongTestCase(TestCase):

    def setUp(self):
        self.publish = Song.objects.create(
            title='Publish', slug='publish', publish=True)

        self.draft = Song.objects.create(title='Draft', slug='draft')

    def test_url_uses_slug(self):
        self.assertEqual(self.publish.get_absolute_url(), '/songs/publish/')

    def test_can_view_published_songs(self):
        response = self.client.get('/songs/publish/')
        song = response.context['song']
        self.assertEquals(self.publish, song)

    def test_detail_uses_template(self):
        response = self.client.get('/songs/publish/')
        self.assertTemplateUsed(response, 'music/song_detail.html')

    def test_cant_view_draft_songs(self):
        response = self.client.get('/songs/draft/')
        self.assertEqual(response.status_code, 404)

    def test_list_returns_published_songs(self):
        response = self.client.get('/songs/')
        song_list = response.context['song_list']
        self.assertIn(self.publish, song_list)
        self.assertNotIn(self.draft, song_list)

    def test_list_uses_template(self):
        response = self.client.get('/songs/')
        self.assertTemplateUsed(response, 'music/song_list.html')


class VideoTestCase(TestCase):

    def setUp(self):
        self.publish = Video.objects.create(
            title='Publish', slug='publish', publish=True)

        self.draft = Video.objects.create(title='Draft', slug='draft')

    def test_url_uses_slug(self):
        self.assertEqual(self.publish.get_absolute_url(), '/videos/publish/')

    def test_can_view_published_videos(self):
        response = self.client.get('/videos/publish/')
        video = response.context['video']
        self.assertEquals(self.publish, video)

    def test_detail_uses_template(self):
        response = self.client.get('/videos/publish/')
        self.assertTemplateUsed(response, 'music/video_detail.html')

    def test_cant_view_draft_videos(self):
        response = self.client.get('/videos/draft/')
        self.assertEqual(response.status_code, 404)

    def test_list_returns_published_videos(self):
        response = self.client.get('/videos/')
        video_list = response.context['video_list']
        self.assertIn(self.publish, video_list)
        self.assertNotIn(self.draft, video_list)

    def test_list_uses_template(self):
        response = self.client.get('/videos/')
        self.assertTemplateUsed(response, 'music/video_list.html')


class LyricsTestCase(TestCase):

    # TODO: TrackFactory?
    def setUp(self):
        # Test a release with published and draft tracks

        self.release = PublishedReleaseFactory.create(
            title='Release', slug='release'
        )

        self.tracks = [
            PublishedSongFactory.create(release=self.release, track=t)
            for t in range(1, 5)
        ]

        for t in range(5, 10):
            SongFactory.create(release=self.release, track=t)

        # Add another release to make sure its tracks are isolated

        second_release = PublishedReleaseFactory.create(
            title='Second Release', slug='second-release'
        )

        for t in range(1, 5):
            PublishedSongFactory.create(release=second_release, track=t)

    def test_url_uses_slug(self):
        self.assertEqual(self.release.get_lyrics_url(),
                         '/music/release/lyrics')

    def test_returns_published_tracks(self):
        response = self.client.get(self.release.get_lyrics_url())

        release = response.context['release']
        self.assertEqual(release, self.release)
        self.assertEqual(list(release.tracks), list(self.tracks))

    def test_uses_template(self):
        response = self.client.get(self.release.get_lyrics_url())
        self.assertTemplateUsed(response, 'music/release_lyrics.html')


class PressTestCase(TestCase):

    def setUp(self):
        self.publish = PublishedPressFactory.create()
        self.draft = PressFactory.create()

    def test_list_returns_published_press(self):
        response = self.client.get(reverse('press_list'))
        press_list = response.context['press_list']
        self.assertIn(self.publish, press_list)
        self.assertNotIn(self.draft, press_list)

    def test_list_uses_template(self):
        response = self.client.get(reverse('press_list'))
        self.assertTemplateUsed(response, 'music/press_list.html')
