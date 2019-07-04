from django.views.generic.list import ListView

from .models import Gig


class GigListView(ListView):
    """
    Renders a list of published ``Gig``'s.
    """
    queryset = Gig.objects.published()
