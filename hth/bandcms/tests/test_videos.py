from datetime import datetime

from django.test import TestCase, override_settings
from django.utils import timezone
from django.core.urlresolvers import reverse

from ..models import AbstractCmsModel, Video, Release


@override_settings(ROOT_URLCONF='bandcms.urls')
class ModelTestCase(TestCase):

    def test_video_is_cms_model(self):
        self.assertTrue(issubclass(Video, AbstractCmsModel))

    def test_can_save_video(self):
        s = Video(title='First', slug='first')
        s.save()

        s1 = Video.objects.get(slug='first')
        self.assertEqual(s, s1)

    def test_video_can_have_details(self):
        s = Video(title='First', slug='first',
                  source_url='http://youtube.com', embed_code='<iframe />',
                  description='Description', credits='credits')
        s.full_clean()
        s.save()

    def test_videos_ordered_by_date(self):
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

    def test_videos_can_be_added_to_release(self):
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

    # TODO: Move to UrlTestCase
    def test_url_uses_slug(self):
        s = Video(title='First', slug='first')
        s.save()

        self.assertEqual(s.get_absolute_url(), '/videos/first/')


# TODO: Create a base UrlTestCase?
@override_settings(ROOT_URLCONF='bandcms.urls')
class UrlTestCase(TestCase):

    def setUp(self):
        publish = Video(title='Published', slug='published', publish=True)
        publish.save()

        draft = Video(title='Draft', slug='draft')
        draft.save()

    def test_can_view_published_videos(self):
        response = self.client.get(reverse('video_detail', args=['published']))
        self.assertTemplateUsed(response, 'bandcms/video_detail.html')
        self.assertContains(response, 'Published')

    def test_cant_view_draft_videos(self):
        response = self.client.get(reverse('video_detail', args=['draft']))
        self.assertEqual(response.status_code, 404)

    def test_list_shows_published_videos(self):
        response = self.client.get(reverse('video_list'))
        self.assertTemplateUsed(response, 'bandcms/video_list.html')
        self.assertContains(response, 'Published')
        self.assertNotContains(response, 'Draft')

