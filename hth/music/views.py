from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Release


class ReleaseListView(ListView):
    queryset = Release.published.all()


class ReleaseDetailView(DetailView):
    queryset = Release.published.all()

