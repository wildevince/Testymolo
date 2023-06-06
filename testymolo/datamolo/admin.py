from django.contrib import admin

import datamolo.models as models

# Register your models here.
admin.site.register(models.Modulo)
admin.site.register(models.Profile)
admin.site.register(models.Organism)
admin.site.register(models.Genome)
admin.site.register(models.Protein)
admin.site.register(models.CDS)
admin.site.register(models.PolyProtein)
admin.site.register(models.Subseq)
admin.site.register(models.Structure)
admin.site.register(models.Annotation)