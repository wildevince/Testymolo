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


    prot_ac = 375
    protein = data.Protein.objects.get(data_ac=prot_ac, derivedFromPP=False)
    subseq_list:list = data.Subseq.objects.filter(origin=protein)
    #modulo_list:list = [subseq.profile.modulo for subseq in subseq_list]
    
    context["data"] = { 
        "protein": data.Protein.serialize(protein), 
        "subseq": [data.Subseq.serialize(subseq) for subseq in subseq_list],
        #"modulo": [data.Modulo.serialize(module) for module in modulo_list],
        #"subseq": {str(j): data.Subseq.serialize(subseq) for j, subseq in enumerate(subseq_list)},
        #"modulo": {str(j): data.Modulo.serialize(module) for j, module in enumerate(modulo_list)},
        }
    #print("BASE_DIR", settings.BASE_DIR)
    #print("STATIC_ROOT", settings.STATIC_ROOT)

    #return HttpResponse("The World !")
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