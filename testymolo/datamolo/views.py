from django.shortcuts import render
from django.http import HttpResponse


import datamolo.scr.add_item_in_model as scr


# Create your views here.

def index(request):

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
    ### need to flush and restart
    scr.parse_data()



    return HttpResponse("The World !")
