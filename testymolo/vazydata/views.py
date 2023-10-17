import os

from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse

import datamolo.scr.database as db
import datamolo.models as data

from vazydata.forms import OrganismForm, ProteinFrom


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
    
    resume_Organism:data.Organism = None


    def next_Protein():
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

    def run_taxonkit(request, taxid):
        return HttpResponse(db.run_taxonkit(taxid))

    def parse_vazy_data_1(request, taxid):
        Vazy1:dict = {'Organism':[], 'CAZy_DB':[]}
        for item in Database.vazy_data_1['Organism']:
            if taxid == item[0]:
                Vazy1['Organism'].append(item)
        for item in Database.vazy_data_1['CAZy_DB']:
            if taxid == item[5]:
                Vazy1['CAZy_DB'].append(item)
        return HttpResponse(db.parse_vazy_data_1(Vazy1))

    def index(request, context:dict={}):
        context['numbers'] = Database.paintedByNumbers()
        
        if Database.resume_Organism is not None:
            resume_last = Database.resume_Organism
            context['resume'] = True
            
        else :
            ToDoList:list = data.Organism.objects.filter(complete=False)
            if len(ToDoList) > 0:
                resume_last = ToDoList[0]
                Database.resume_Organism = resume_last

        context['object_id'] = resume_last.id
        context['form'] = OrganismForm(initial=resume_last.serialize(False))
        proteins = data.Protein.objects.filter(organism=resume_last)
        proteinForm:list = []
        for prot in proteins:
            prot_init = prot.serialize(False) 
            prot_init['genbank'] = "null" ### debug
            proteinForm.append(ProteinFrom(initial=prot_init))
        context["proteinForm"] = proteinForm

        #context['taxonkit'] =  Database.run_taxonkit(request, str(resume_last.id))

        print(*context)
        return render(request, Database.template_name, context) 
    
    def big_POST(request):
        context:dict={}
        if request.method == "POST":
            return HttpResponse('You caught a POKEMON !')
            form_org = VazyRecord(request.POST, prefix="Organism")
            if form.is_valid():
                _id = form.cleaned_data['id']
                _name = form.cleaned_data['name']
                _abr = form.cleaned_data['abr']
                _phylogeny = form.cleaned_data['phylogeny']
                _genome = form.cleaned_data['genome']
                return 
            
        return HttpResponse("Damn! The wild POKEMON escaped ...")
    
    def POST_protein(request):
        return HttpResponse("You caught a fish !")
        pass
    
    def add_form_Protein():
        form = ProteinFrom()
        response:str = "<form method='post' action='/resumedb/protein/'>"
        response += form.as_p()
        response += "<input type='submit' name='Protein' value='Completed'></form>"
        HttpResponse(response)