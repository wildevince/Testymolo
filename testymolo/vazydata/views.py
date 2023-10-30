import os

from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from django.http import HttpResponse

import datamolo.scr.database as db
import datamolo.models as data

from vazydata.forms import OrganismForm, ProteinFrom


# Create your views here.
class Database(TemplateView):

    template_name = os.path.join("vazydata", "resumedb.html")
    template_form_protein = os.path.join("vazydata", "form_protein.html")
    template_add_form_protein = os.path.join("vazydata", "add_form_protein.html")
    vazy_data_1:dict = {
        'Organism': db.read_data_1('Organism'),
        'CAZy_DB': db.read_data_1('CAZy_DB'),
    }

    vazy_data_2:dict = {
        'Organism.temp': db.read_data_2('Organism.temp'),
        'Protein.temp': db.read_data_2('Protein.temp'),
        }
    
    resume_Organism:data.Organism = None
    ongoing_blastp:str = None

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
        org = resume_last.serialize(False)
        org['id_hide'] = resume_last.id
        org['name_hide'] = resume_last.name
        org['abr_hide'] = resume_last.abr
        org['phylogeny_hide'] = resume_last.phylogeny
        context['form'] = OrganismForm(initial=org)
        proteins = data.Protein.objects.filter(organism=resume_last)
        proteinForm:list = []
        for prot in proteins:
            prot_init = prot.serialize(False) 
            prot_init['id'] = prot.id
            prot_init['genbank'] = "null" ### debug
            prot_init['subseqs'] = len(data.Subseq.objects.filter(origin=prot)) 
            prot_init['fasta'] = '>' + str(prot.header) + '\n' + str(prot.sequence)
            prot_init['fasta_hide'] = prot_init['fasta']
            prot_init['genbank_hide'] = prot_init['genbank']
            prot_init['name_hide'] = prot_init['name']
            ### 
            proteinForm.append(ProteinFrom(initial=prot_init))
            break
        context["proteinForm"] = proteinForm
        return render(request, Database.template_name, context) 
    
    def big_POST(request):
        context:dict={}
        if request.method == "POST":
            #return HttpResponse('You caught a POKEMON !')
            form = OrganismForm(request.POST)
            if form.is_valid():
                _id_hide = form.cleaned_data['id_hide']
                _name_hide = form.cleaned_data['name_hide']
                _abr_hide = form.cleaned_data['abr_hide']
                _phylogeny_hide = form.cleaned_data['phylogeny_hide']
                #
                _id = form.cleaned_data['id']
                _name = form.cleaned_data['name']
                _abr = form.cleaned_data['abr']
                _phylogeny = form.cleaned_data['phylogeny']

                print(_id_hide, _name_hide, _abr_hide, _phylogeny_hide[-5:])
                print(_id, _name, _abr, _phylogeny[-5:])
                org = data.Organism.objects.get(id=_id_hide)
                if not (_id == _id_hide): # taxid changed !
                    print("taxid changed", _id_hide, "into", _id)
                    if len(data.Organism.objects.filter(id = _id)) == 0:
                        org.id = _id
                        # quid of Protein.organism
                if not (_name == _name_hide): 
                    print("changed", _name_hide, 'into', _name)
                    org.name = _name
                if not (_abr == _abr_hide):
                    print("changed", _abr_hide, 'into', _abr)
                    org.abr = _abr
                if not (_phylogeny == _phylogeny_hide):
                    print("changed", _phylogeny_hide[-10:], 'into', _phylogeny[-10:])
                    org.phylogeny = _phylogeny
                ## no change
                resume_Organism = None
                org.complete = True
                ###org.save()
                return HttpResponse("cleaning fields")
            else:
                print(form.errors)
                return HttpResponse("error form")
            
        return HttpResponse("Damn! The wild POKEMON escaped ...")
    
    def POST_protein(request):
        context:dict = {}
        if request.method == "POST":
            form = ProteinFrom(request.POST)
            if form.is_valid():
                _id = form.cleaned_data['id']
                _subseqs = form.cleaned_data['subseqs']
                _fasta = form.cleaned_data['fasta']
                _isPP = form.cleaned_data['isPP']
                _derivedFromPP = form.cleaned_data['derivedFromPP']
                _organism = form.cleaned_data['organism']
                _genbank = form.cleaned_data['genbank']
                _name = form.cleaned_data['name']
                _data_ac = form.cleaned_data['data_ac']

                _fasta_hide = form.cleaned_data['fasta_hide']
                _genbank_hide = form.cleaned_data['genbank_hide']
                _name_hide = form.cleaned_data['name_hide']

                print(_id,_subseqs,_fasta[:5],_isPP,_derivedFromPP,str(_organism),_genbank,_name,_data_ac )
                prot = data.Protein.objects.get(id=_id)
                if not (_fasta == _fasta_hide):
                    print("changed fasta sequence")
                    header, *sequence = _fasta.split()
                    prot.header = header
                    prot.sequence = sequence
                if not (_genbank == _genbank_hide):
                    prot.genbank = _genbank
                if not (_name == _name_hide):
                    prot.name = _name

                prot.complete = True
                ###prot.save()
                return Database.index(request)
            else:
                print(form.errors)
                
        return HttpResponse("ERROR : My precious ...")
    
    def add_form_Protein(request):
        ## add csrf_token
        #<button onclick='add_form_Protein()'>Add Protein</button>
        #<span id='add_form_Protein'></span>
        response = render_to_string(Database.template_add_form_protein, {'prot': ProteinFrom()})
        return HttpResponse(response)
    
    def blastp_inquiry(request, _id):
        if _id is not None:
            prot = data.Protein.objects.get(id=_id)
            fasta = '>'+prot.header+'\n'+prot.sequence
            
            Database.ongoing_blastp = db.run_diamond_blatp(fasta)

            answer = HttpResponse()
            answer.set_cookie('ongoing_blastp', Database.ongoing_blastp)
            return answer
        
    def blastp_response(request):
        cookie = request.COOKIES.get('ongoing_blastp')
        # if file ready
        # True : return data
        # False : return waiting message