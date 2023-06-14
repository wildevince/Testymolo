import os

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings


import datamolo.scr.add_item_in_model as scr
import datamolo.models as data



# Create your views here.

def index(request):

    template_name:str = os.path.join("datamolo", "main.html")
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

    context['data'] = []

    def get_random_protein():
        import random
        PROTEINS = data.Protein.objects.filter(derivedFromPP=False)
        N:int = len(PROTEINS)
        i = random.randint(1, N-1)
        return PROTEINS[i]

    for k in range(2):
        protein = get_random_protein()
        print("protein: "+str(protein.data_ac))
        subseq_list = data.Subseq.objects.filter(origin=protein)
        context['data'].append({
            "protein": data.Protein.serialize(protein), 
            "subseq": [data.Subseq.serialize(subseq) for subseq in subseq_list],
        })


    return render(request, template_name, context)



# works !
def download(request):
    dirpath = os.path.join(settings.MEDIA_ROOT, 'data', 'sequences.fasta')
    if(os.path.exists(dirpath)):
        handle = open(dirpath, 'r')
        response = HttpResponse(handle, content_type=dirpath)
        response['Content-Disposition'] = f"attachment; filename=sequences.fasta"
        return response
    return HttpResponse("not found")