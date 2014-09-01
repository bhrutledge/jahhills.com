from datetime import datetime

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone

from core.models import PublishedModel
from ..models import Release, Song, Video


class ReleaseTestCase(TestCase):

    def test_can_be_published(self):
        self.assertTrue(issubclass(Release, PublishedModel))

    def test_required_fields(self):
        required_fields = set(['title', 'slug'])

        with self.assertRaises(ValidationError) as cm:
            Release().full_clean()

        blank_fields = set(cm.exception.message_dict.keys())
        self.assertEquals(required_fields, blank_fields)

    def test_can_be_saved(self):
        r = Release(title='First', slug='first')
        r.full_clean()
        r.save()

        r1 = Release.objects.get(slug='first')
        self.assertEqual(r, r1)

    def test_can_have_details(self):
        r = Release(title='First', slug='first', date='2014-08-01',
                    cover_url='http://placehold.it/640',
                    description='Description', credits='Credits')
        r.full_clean()
        r.save()

    def test_ordered_by_date(self):
        first = Release(title='First', slug='first', date='2014-08-01')
        first.save()

        old = Release(title='Older', slug='older', date='2014-07-31')
        old.save()

        new = Release(title='Newer', slug='newer', date='2014-08-31')
        new.save()

        self.assertEqual(list(Release.objects.all()), [new, first, old])


class SongTestCase(TestCase):

    def test_can_be_published(self):
        self.assertTrue(issubclass(Song, PublishedModel))

    def test_required_fields(self):
        required_fields = set(['title', 'slug'])

        with self.assertRaises(ValidationError) as cm:
            Song().full_clean()

        blank_fields = set(cm.exception.message_dict.keys())
        self.assertEquals(required_fields, blank_fields)

    def test_can_be_saved(self):
        s = Song(title='First', slug='first')
        s.save()

        s1 = Song.objects.get(slug='first')
        self.assertEqual(s, s1)

    def test_song_can_have_details(self):
        s = Song(title='First', slug='first',
                 description='Description', credits='Credits', lyrics='Lyrics')
        s.full_clean()
        s.save()

    def test_ordered_by_title(self):
        first = Song(title='First', slug='first')
        second = Song(title='Second', slug='second')
        third = Song(title='Third', slug='third')

        third.save()
        first.save()
        second.save()

        self.assertEqual(list(Song.objects.all()), [first, second, third])

    def test_tracks_can_be_added_to_release(self):
        r = Release(title='Release', slug='release')
        r.save()

        publish = Song(title='Publish', slug='publish', release=r, track=1,
                       publish=True)
        publish.save()

        draft = Song(title='Draft', slug='draft', release=r, track=2)
        draft.save()

        tracks = list(r.tracks.all())
        self.assertIn(publish, tracks)
        self.assertNotIn(draft, tracks)

    def test_tracks_ordered_by_number(self):
        r = Release(title='Release', slug='release')
        r.save()

        s1 = Song(title='Z Song', slug='z', release=r, track=1, publish=True)
        s2 = Song(title='B Song', slug='b', release=r, track=2, publish=True)
        s3 = Song(title='A Song', slug='a', release=r, track=3, publish=True)

        s3.save()
        s1.save()
        s2.save()

        self.assertEqual(list(r.tracks.all()), [s1, s2, s3])


class VideoTestCase(TestCase):

    def test_can_be_published(self):
        self.assertTrue(issubclass(Video, PublishedModel))

    def test_required_fields(self):
        required_fields = set(['title', 'slug'])

        with self.assertRaises(ValidationError) as cm:
            Video().full_clean()

        blank_fields = set(cm.exception.message_dict.keys())
        self.assertEquals(required_fields, blank_fields)

    def test_can_be_saved(self):
        s = Video(title='First', slug='first')
        s.save()

        s1 = Video.objects.get(slug='first')
        self.assertEqual(s, s1)

    def test_can_have_details(self):
        s = Video(title='First', slug='first',
                  source_url='http://youtube.com', embed_code='<iframe />',
                  preview_url='http://youtube.com/jpg',
                  description='Description', credits='credits')
        s.full_clean()
        s.save()

    def test_ordered_by_date(self):
        draft = Video(title='Draft', slug='draft')
        draft.save()

        first = Video(title='First', slug='first', publish=True,
                      publish_on=datetime(2014, 7, 22, tzinfo=timezone.utc))
        first.save()

        old = Video(title='Old', slug='old', publish=True,
                    publish_on=datetime(2014, 7, 21, tzinfo=timezone.utc))
        old.save()

        new = Video(title='New', slug='new', publish=True,
                    publish_on=datetime(2014, 7, 23, tzinfo=timezone.utc))
        new.save()

        self.assertEqual(list(Video.objects.all()), [draft, new, first, old])

    def test_can_be_added_to_release(self):
        r = Release(title='Release', slug='release')
        r.save()

        publish = Video(title='Publish', slug='publish', release=r,
                        publish=True)
        publish.save()

        draft = Video(title='Draft', slug='draft', release=r)
        draft.save()

        videos = list(r.videos.all())
        self.assertIn(publish, videos)
        self.assertNotIn(draft, videos)

        # TODO: test ordered by date?

