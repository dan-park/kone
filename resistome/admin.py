from django.contrib import admin
from resistome.models import Biome, Sample, RawFiles, ARG

# Register your models here.
admin.site.register(Biome)
admin.site.register(Sample)
admin.site.register(RawFiles)
admin.site.register(ARG)