import os

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
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

    """
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
    """

    return render(request, template_name, context)




def load_figure(request):
    # AJAX

    def get_random_protein():
        import random
        PROTEINS = data.Protein.objects.filter(derivedFromPP=False)
        N:int = len(PROTEINS)
        i = random.randint(1, N-1)
        print("protein: "+str(PROTEINS[i]))
        return PROTEINS[i]
    protein = get_random_protein()

    ## generate figure
    real_WIDTH = 1860
    WIDTH = 1800
    x0 = 30
    html:str = ""
    chtext:bool = False
    chlvl:int = 0

    organism = protein.organism
    L = len(protein.sequence)
    
    html += f"<svg width='{str(real_WIDTH)}' height='400'> \n"
    html += f"<rect id='background' width='100%' height='100%' fill='grey' fill-opacity='0.1' stroke='black' /> \n"
    html += f"<rect id='protein' x='{x0}' y='40%' width='{WIDTH}' height='20%' fill='blue' fill-opacity='0.1'/> \n"
    text1 = f"name:{protein.name},    polyprotein:{protein.isPP},  derived from polyprotein:{protein.derivedFromPP}"
    text2 = f"organism:{organism.name},    acc:{protein.data_ac},    length:{L}"
    html += f"<text x='10' y='5%' >{text1}</text>\n"
    html += f"<text x='10' y='10%' >{text2}</text>\n"

    i=0
    Subseqs = data.Subseq.objects.filter(origin=protein)
    for subseq in Subseqs:
        i+=1
        lenseq = len(protein.sequence[subseq.start:subseq.end])
        w = (lenseq / L) * WIDTH
        x = (subseq.start-1)/L *WIDTH +x0

        html += f"<rect class='subseq' id='subseq_{i}' height='20%' y='40%' fill='blue' fill-opacity='0.2' "
        html += f"x='{x}' width='{w}' />\n"
        if(w < (0.020 *WIDTH)):
            chtext = True
            chlvl += 1  
        else:
            chlvl = chlvl-1 if(chlvl > 0) else 0

        #text module_name
        if(w > (0.020 *WIDTH)):
            x += w*2/5
        y = 35
        if(chtext):
            y -= (4 *chlvl)
        if(subseq.profile):
            module = subseq.profile.modulo.id 
        else:
            module = "unknown"
        html += f"<text class='module_name' id='module_name_{i}' font-size='14' y='{y}%' "
        html += f"x='{x}' >{module}</text>\n"

        #line separator
        x1 = ((subseq.end-1) / L) *WIDTH +x0
        html += f"<line class='separator' id='separator_{i}' y1='40%' y2='60%' stroke='black' stroke-width='2' "
        html += f"x1='{x1}' x2='{x1}' />\n"

        #text numbering
        if(i < len(Subseqs)):
            y = 65
            if(chtext):
                chtext = False
                y += (4 *chlvl)
            x = ((subseq.end -1) / L) *WIDTH +x0
        else:
            text_length:int = len(str(subseq.end))
            y = 70 + 5 *chlvl
            x = (real_WIDTH - text_length *10)
        html += f"<text class='numbering' id='numbering_{i}' font-size='10'  "
        html += f" y='{y}%' x='{x}' >{subseq.end -1}</text>\n"
    html += "</svg>"

    return HttpResponse(html)






# works !
def download(request):
    dirpath = os.path.join(settings.MEDIA_ROOT, 'data', 'sequences.fasta')
    if(os.path.exists(dirpath)):
        handle = open(dirpath, 'r')
        response = HttpResponse(handle, content_type=dirpath)
        response['Content-Disposition'] = f"attachment; filename=sequences.fasta"
        return response
    return HttpResponse("not found")