import os

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.views.generic import TemplateView
from django.utils.safestring import mark_safe


import datamolo.scr.add_item_in_model as scr
import datamolo.scr.figures as fig

import datamolo.models as data



# Create your views here.
class Main(TemplateView):
    template_name = os.path.join("datamolo", "main.html")
    moduleCard_template = os.path.join("datamolo", "moduleCard.html")
    mainfocus_protein = None
    mainfocus_profile = None
    mainminus_protein = []
    module = None
    phylo = None
    subseq = None
    profile = None


    def index(request):

        context:dict = {}

        ## implement Database
        
        ### Organism , Protein , Subseq 
        ###scr.parse_data()  #-> done

        ### Modulo
        ###scr.parse_Modules()  #-> done

        ### Structure
        ### lack info

        ### link between Modulo--Subeq
        ### Subseq --+ Profile -1-1- Modulo   (facile => aggregation && one-to-one )
        ### Subseq +-- Annotation --* Modulo  (difficile => positioning within limits && sorting types of annotation)

        ### Subseq --+ Profile -1-1- Modulo   (facile => aggregation && one-to-one )


        ### need to hard flush and restart 
        #scr.parse_data() 
        
        ### BACKUP

        #Table_names = [tab[0] for tab in data.Annotation.Tables_SQL]
        #scr.parse_Annotations(Table_names) 

        ### BACKUP 2

        ### -> visualization JS tool !
        ### question: protein 375 -> polyprotein 1ab du HCoV

        context:dict = {}

        if(Main.mainfocus_profile):
            context['Profile'] = "<p>work in progress</p>"
        elif(Main.mainfocus_protein):
            context['Protein'] = fig.generate_mainfigure_protein
        
        if(len(Main.mainminus_protein) >= 0):
            html:str = ""
            for protein_id in Main.mainminus_protein:
                html += fig.generate_minusfigure_protein(data.Protein.objects.get(id=protein_id)) + '\n'
            context['proteins'] = mark_safe(html)
        
        if(Main.module):
            Main.module = None
            #context['Module'] = Main.load_card_module(request, Main.subseq)

        if(Main.phylo):
            Main.phylo = None
            #context['Phylo'] = "<p>work in progress</p>"

        return render(request, Main.template_name, context)


    def load_mainfigure_protein(request):
        # AJAX
        def get_random_protein():
            import random
            PROTEINS = data.Protein.objects.filter(derivedFromPP=False)
            N:int = len(PROTEINS)
            i = random.randint(1, N-1)
            print("protein: "+str(PROTEINS[i]))
            return PROTEINS[i]
        protein = get_random_protein()

        Main.mainfocus_protein = protein.id
        Main.mainfocus_profile = None

        updated_html:str = ""
        updated_html = fig.generate_mainfigure_protein(protein)

        return HttpResponse(updated_html)


    def load_plusfigure_protein(request, protein_id):
        #ajax POST

        Main.mainfocus_profile = None
        
        if(protein_id not in Main.mainminus_protein):
            Main.mainminus_protein.append(protein_id)

        protein = data.Protein.objects.get(id=protein_id)
        updated_html:str = fig.generate_mainfigure_protein(protein)
        
        return HttpResponse(updated_html)

        
    def load_minusfigure_protein(request):
        #Ajax

        protein = data.Protein.objects.get(id=Main.mainfocus_protein)
        
        if(protein.id not in Main.mainminus_protein):
            Main.mainminus_protein.append(Main.mainfocus_protein)
        Main.mainfocus_protein = None

        updated_html:str= ""

        updated_html = fig.generate_minusfigure_protein(protein)

        return HttpResponse(updated_html)


    def load_card_module(request, subseq_id):
        #ajax
        context:dict = {}
        Main.subseq = subseq_id
        subseq = data.Subseq.objects.get(id=subseq_id)
        if(subseq.profile):
            Main.module = subseq.profile.modulo.id
            module = data.Modulo.objects.get(id=Main.module)
            context['module'] = module
            context['subseq'] = subseq
            context['profile_id'] = subseq.profile.id
            context['profile_length'] = len(data.Subseq.objects.filter(profile=subseq.profile))
            context['Structures'] = [structure for structure in data.Structure.objects.filter(modulo=subseq.profile.modulo)]
            context['commun_ancestor'] = "'...'"

            return render(request, Main.moduleCard_template, context)
        
        return mark_safe("<p>Don't get ahead of yourself dude !</p>")


    def load_mainfigure_profile(request, profile_id):
        #ajax
        context:dict = {}   
        profile = data.Profile.objects.get(id=profile_id)
        # gather all subseq.sequence when subseq.profile = profile
        Subseqs:dict = {}
        for subseq in data.Subseq.objects.filter(profile=profile):
            Subseqs[str(subseq.id)] = {'header': subseq.header() ,'sequence':subseq.sequence}
        context['subseq'] = Subseqs
        
        return HttpResponse(fig.generate_mainfigure_profile(context))


    # works !
    def download(request):
        dirpath = os.path.join(settings.MEDIA_ROOT, 'data', 'sequences.fasta')
        if(os.path.exists(dirpath)):
            handle = open(dirpath, 'r')
            response = HttpResponse(handle, content_type=dirpath)
            response['Content-Disposition'] = f"attachment; filename=sequences.fasta"
            return response
        return HttpResponse("not found")