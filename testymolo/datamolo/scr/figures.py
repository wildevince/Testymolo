from django.http import HttpResponse
import datamolo.models as data



def generate_mainfigure_protein(protein:data.Protein):

    ## generate figure
    real_WIDTH = 1860
    WIDTH = 1800
    x0 = 30
    html:str = ""
    chtext:bool = False
    chlvl:int = 0

    organism = protein.organism
    L = len(protein.sequence)
    
    
    html += f"<div><button class='minus' onclick='updateSection_figure_minus()'>-</button></div>\n"
    html += f"<div><svg protein={protein.id} width='{str(real_WIDTH)}' height='400'> \n"
    html += f"<rect class='background' width='100%' height='100%' fill='grey' fill-opacity='0.1' stroke='black' /> \n"
    html += f"<rect class='protein' x='{x0}' y='40%' width='{WIDTH}' height='20%' fill='blue' fill-opacity='0.1'/> \n"
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

        html += f"<rect class='subseq' id='{subseq.id}' height='20%' y='40%' fill='blue' fill-opacity='0.2' "
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
    html += "</svg></div>"

    return '<div>'+html+'</div>'


def generate_minusfigure_protein(protein:data.Protein):
    html:str = ""
    WIDTH = 1000

    organism = protein.organism
    L = len(protein.sequence)

    html += f"<div><button class='plus' onclick='updateSection_figure_plus({protein.id})'>+</button></div>\n"
    html += f"<div><svg protein={protein.id} width={WIDTH} height='150'>"
    html += f"<rect id='background' width='100%' height='100%' fill='grey' fill-opacity='0.1' stroke='black' /> \n"
    html += f"<rect id='protein' y='60%' width='100%' height='25%' fill='blue' fill-opacity='0.1'/> \n"
    text1 = f"name:{protein.name},    polyprotein:{protein.isPP},  derived from polyprotein:{protein.derivedFromPP}"
    text2 = f"organism:{organism.name},    acc:{protein.data_ac},    length:{L}"
    html += f"<text x='10' y='15%' >{text1}</text>\n"
    html += f"<text x='10' y='30%' >{text2}</text>\n"

    i=0
    Subseqs = data.Subseq.objects.filter(origin=protein)
    for subseq in Subseqs:
        #line separator
        i += 1
        x1 = ((subseq.end-1) / L) *WIDTH
        html += f"<line class='separator' id='separator_{i}' y1='60%' y2='85%' stroke='black' stroke-width='2' "
        html += f"x1='{x1}' x2='{x1}' />\n"

    html += "</svg></div>"

    return '<div>'+html+'</div>'

