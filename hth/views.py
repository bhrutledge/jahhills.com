from django.views.generic import TemplateView

from hth.news.models import Post
from hth.shows.models import Gig
from hth.music.models import Release, Video


class HomePageView(TemplateView):
    """
    Renders the home page.
    """
    template_name = 'home_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['post'] = Post.objects.published().first()
        context['gig_list'] = Gig.objects.published().upcoming()
        context['release'] = Release.objects.published().first()
        context['video'] = Video.objects.published().first()

        return context


class AboutPageView(TemplateView):
    """
    Renders the about page.
    """
    template_name = 'about_page.html'
