from datetime import datetime, timezone

import factory
import factory.fuzzy


class DraftPostFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'news.Post'

    slug = factory.Sequence(lambda n: 'post-%d' % n)
    title = factory.Sequence(lambda n: 'Post %d' % n)
    body = factory.fuzzy.FuzzyText(length=100)


class PublishedPostFactory(DraftPostFactory):

    publish = True
    publish_on = factory.fuzzy.FuzzyDateTime(
        datetime(2000, 1, 1, tzinfo=timezone.utc))
