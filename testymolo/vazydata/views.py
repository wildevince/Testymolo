import os

from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse

import datamolo.scr.database as db
import datamolo.models as data

from vazydata.forms import ProteinForm


# Create your views here.
class Database(TemplateView):

    template_name = os.path.join("vazydata", "resumedb.html")
    vazy_data_1:dict = {
        'Organism': db.read_data_1('Organism'),
        'CAZy_DB': db.read_data_1('CAZy_DB'),
    }

    vazy_data_2:dict = {
        'Organism.temp': db.read_data_2('Organism.temp'),
        'Protein.temp': db.read_data_2('Protein.temp'),
        }


    def next_Protein():
        ## protein
        ToDoList:list = data.Protein.objects.filter(complete=False)
        if len(ToDoList) > 0:
            return ToDoList[0]
        return None
  

    def next(request, Table:str='Protein'):
        context:dict = {}

        # treat POST request
        if request.method == "POST":
            print("YOU CAUGHT A POKEMON !")
            form = ProteinForm(request.POST)
            if form.is_valid():
                ## update model item
                pass

        # next one
        item = Database.next_Protein()
        if not item is None:
            context['form'] = ProteinForm(instance=item)
            context['object_id'] = item.id
        
        return Database.index(request, context)

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


    def run_taxonkit(request, taxid):
        return HttpResponse(db.run_taxonkit(taxid))


    def index(request, context:dict={}):
        context['numbers'] = Database.paintedByNumbers()

        """
        if request.method == "POST":
            form = ProteinForm(request.POST)
            if form.is_valid():
                return 
        else :
            form = ProteinForm()
        context['form'] = form
        """
        
        print(context)
        return render(request, Database.template_name, context) 
    