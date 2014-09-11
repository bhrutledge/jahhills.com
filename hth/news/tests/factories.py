import factory
import factory.fuzzy


class PostFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'news.Post'

    slug = factory.Sequence(lambda n: 'post-%d' % n)
    title = factory.Sequence(lambda n: 'Post %d' % n)
    body = factory.fuzzy.FuzzyText(length=100)
