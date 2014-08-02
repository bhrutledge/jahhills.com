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

    @override_settings(ROOT_URLCONF='bandcms.urls.releases')
    def test_url_uses_slug(self):
        s = Song(title='First', slug='first')
        s.save()

        self.assertEqual(s.get_absolute_url(), '/songs/first/')


@override_settings(ROOT_URLCONF='bandcms.urls.releases')
class UrlTestCase(TestCase):

    def setUp(self):
        publish = Song(title='Published', slug='published', publish=True)
        publish.save()

        draft = Song(title='Draft', slug='draft')
        draft.save()

    def test_can_view_published_songs(self):
        response = self.client.get(reverse('song_detail', args=['published']))
        self.assertTemplateUsed(response, 'bandcms/song_detail.html')
        self.assertContains(response, 'Published')

    def test_cant_view_draft_songs(self):
        response = self.client.get(reverse('song_detail', args=['draft']))
        self.assertEqual(response.status_code, 404)

    def test_list_shows_published_songs(self):
        response = self.client.get(reverse('song_list'))
        self.assertTemplateUsed(response, 'bandcms/song_list.html')
        self.assertContains(response, 'Published')
        self.assertNotContains(response, 'Draft')

