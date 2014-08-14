from django.test import TestCase
from django.core.exceptions import ValidationError

from core.models import PublishedModel
from ..models import Release, Song


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

