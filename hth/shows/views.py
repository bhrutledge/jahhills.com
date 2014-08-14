from django.views.generic.list import ListView

from .models import Gig


class GigListView(ListView):
    queryset = Gig.published.all()

