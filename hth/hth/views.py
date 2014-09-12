from django.views.generic import TemplateView

from news.models import Post


class HomePageView(TemplateView):
    """
    Renders the home page.
    """

    template_name = 'home_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = Post.objects.published().first()
        return context
