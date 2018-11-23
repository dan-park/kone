from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse
from django.core.files import File
from django.views.generic import View, TemplateView, ListView
from resistome.models import Biome, Sample, RawFiles, ARG, SampleToContigs

# Create your views here.
def index(request):
    return HttpResponse("Hello, You're at the resistome index.")


class ContigsView(ListView):
    model = RawFiles
    template_name = "resistome/db_contigs.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

