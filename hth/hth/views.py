from django.views.generic import TemplateView

from news.models import Post
from shows.models import Gig


class HomePageView(TemplateView):
    """
    Renders the home page.
    """

    template_name = 'home_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['post'] = Post.objects.published().first()
        context['gig_list'] = Gig.objects.published().upcoming()

        return context
