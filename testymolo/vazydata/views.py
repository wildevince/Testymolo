import os

from django.shortcuts import render
from django.views.generic import TemplateView

import datamolo.scr.database as db
import datamolo.models as data


# Create your views here.
class Database(TemplateView):

    template_name = os.path.join("vazydata", "resumedb.html")


    def paintedByNumbers():

        def completedTable(table):
            univers = len(table.all())
            if univers == 0 :
                return 0.0
            return int(len(table.filter(complete=True)) / len(table.all()) *10000) / 100.0 

        return {
            "CDS": completedTable(data.CDS.objects),
            "Genome": completedTable(data.Genome.objects),
            "Organism": completedTable(data.Organism.objects),
            "Protein": completedTable(data.Protein.objects),
            "PolyProtein": completedTable(data.PolyProtein.objects),
            "Annotation": completedTable(data.Annotation.objects),
            "Subseq": completedTable(data.Subseq.objects),
            "Modulo": completedTable(data.Modulo.objects),
            "Profile": completedTable(data.Profile.objects),
            "Structure": completedTable(data.Structure.objects),

        }

    
    def index(request):
        context:dict = {'Number': Database.paintedByNumbers()}
        return render(request, Database.template_name, context) 