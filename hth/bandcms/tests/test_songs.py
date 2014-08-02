from django.test import TestCase, override_settings
from django.core.urlresolvers import reverse

from ..models import AbstractCmsModel, Song


class ModelTestCase(TestCase):

    def test_song_is_cms_model(self):
        self.assertTrue(issubclass(Song, AbstractCmsModel))

    def test_can_save_song(self):
        s = Song(title='First', slug='first')
        s.save()

        s1 = Song.objects.get(slug='first')
        self.assertEqual(s, s1)

    def test_song_can_have_details(self):
        s = Song(title='First', slug='first',
                 description='Description', credits='credits', lyrics='Lyrics')
        s.full_clean()
        s.save()

    def test_songs_ordered_by_title(self):
        first = Song(title='First', slug='first')
        second = Song(title='Second', slug='second')
        third = Song(title='Third', slug='third')

        third.save()
        first.save()
        second.save()

        self.assertEqual(list(Song.objects.all()), [first, second, third])

