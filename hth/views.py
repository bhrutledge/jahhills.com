from pathlib import Path
from typing import cast

from django.views.generic import TemplateView
from django.http import Http404
from django.conf import settings

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


class NetlifyTemplateView(TemplateView):
    """
    Maps /{template-name}/ to netlify/templates/{template-name}.html
    """

    def get_template_names(self):
        template_name = self.kwargs.get('template_name')
        if not template_name:
            raise Http404("Template name not provided")

        netlify_templates_dir = (cast(Path, settings.BASE_DIR) / 'netlify' / 'templates').resolve()
        template_file_path = (netlify_templates_dir / f'{template_name}.html').resolve()

        # Verify it's actually in the netlify/templates directory (additional security check)
        # If relative_to() raises ValueError, the file is not within the expected directory
        try:
            template_file_path.relative_to(netlify_templates_dir)
        except ValueError:
            raise Http404("Template not in Netlify templates directory")

        # Verify the file exists in the netlify/templates directory
        if not template_file_path.exists():
            raise Http404(f"{template_name}.html does not exist")

        return [f'{template_name}.html']
