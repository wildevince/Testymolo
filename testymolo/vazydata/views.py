import os

from django.shortcuts import render
from django.views.generic import TemplateView

import datamolo.scr.database as db
import datamolo.models as data

from vazydata.forms import ProteinForm


# Create your views here.
class Database(TemplateView):

    template_name = os.path.join("vazydata", "resumedb.html")

    def next_entity():
        ## protein
        ToDoList:list = data.Protein.objects.filter(complete=False)
        if len(ToDoList) > 0:
            return ToDoList[0]
        return None
  
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
        context:dict = {'number': Database.paintedByNumbers()}

        if request.method == "POST":
            form = ProteinForm(request.POST)
            if form.is_valid():
                return 
        else :
            form = ProteinForm()
        
        context['form'] = form

        return render(request, Database.template_name, context) 