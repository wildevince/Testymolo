import os

from django.shortcuts import render
from django.http import HttpResponse


import datamolo.scr.add_item_in_model as scr
import datamolo.models as data



# Create your views here.

def index(request):

    template_name:str = os.path.join("datamolo", "datamolo.html")
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

    #Table_names = [tab[0] for tab in Annotation.Tables_SQL]
    #scr.parse_Annotations(Table_names) 

    ### BACKUP 2

    ### -> visualization JS tool !
    ### question: protein 375 -> polyprotein 1ab du HCoV

    prot_ac = 375
    protein = data.Protein.objects.get(data_ac=prot_ac, derivedFromPP=False)
    subseq_list = data.Subseq.objects.filter(origin=protein)
    modulo_list = [subseq.profile.modulo for subseq in subseq_list]
    context[str(prot_ac)] = { "protein":protein, "subseq":subseq_list, "modulo":modulo_list }

    #return HttpResponse("The World !")
    return render(request, template_name, context)
