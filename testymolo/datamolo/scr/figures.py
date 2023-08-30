import datamolo.models as data

from Bio import SeqIO
import logomaker as logo


def generate_mainfigure_protein(protein:data.Protein):
    ## generate figure
    real_WIDTH = 1860
    WIDTH = 1800
    x0 = 30
    html:str = ""
    chtext:bool = False
    chlvl:int = 0
    y_top = 50
    y_height = 20

    organism = protein.organism
    L = len(protein.sequence)
    
    html += "<div class='button-container'>"
    #html += "<button class='compare' >Compare with <span class='uni_star' value=false style='color: orange;'>★</span></button>\n"
    html += "<button class='minus' onclick='updateSection_figure_minus()'>-</button></div>\n"
    html += f"<span class='sequence_selected_icon' arrow='arrow-thick-right' ><span class='whitespace'>_</span></span><span class='header'>{protein.header}</span> \n"
    html += f"<div class='svg-container'><svg protein={protein.id} width='{str(real_WIDTH)}' height='300'> \n"
    html += f"<rect class='background' width='100%' height='100%' fill='grey' fill-opacity='0.1' stroke='black' /> \n"
    html += f"<rect class='protein' x='{x0}' y='{y_top}%' width='{WIDTH}' height='{y_height}%' fill='blue' fill-opacity='0.1'/> \n"
    text1 = f"name:{protein.name},    polyprotein:{protein.isPP},  derived from polyprotein:{protein.derivedFromPP}"
    text2 = f"organism:{organism.name},    acc:{protein.data_ac},    length:{L}"
    html += f"<text x='10' y='5%' >{text1}</text>\n"
    html += f"<text x='10' y='15%' >{text2}</text>\n"

    i=0
    Subseqs = data.Subseq.objects.filter(origin=protein)
    for subseq in Subseqs:
        i+=1
        lenseq = len(protein.sequence[subseq.start:subseq.end])
        w = ((lenseq +1) / L) * WIDTH
        x = (subseq.start-1)/L *WIDTH +x0
        # find module
        if(subseq.profile):
            module = subseq.profile.modulo.id 
        else:
            module = "?"
        
        html += f"<rect class='subseq' subseq='{subseq.id}' height='{y_height}%' y='{y_top}%' fill='blue' fill-opacity='0.2' "
        html += f"x='{x}' width='{w}' />\n"
        if(w < (0.020 *WIDTH)):
            chtext = True
            chlvl += 1  
        else:
            chlvl = chlvl-1 if(chlvl > 0) else 0

        #text module_name
        if(w > (0.020 *WIDTH)):
            x += w*2/5
        y = y_top-5
        if(chtext):
            y -= (5 *chlvl)
        html += f"<text class='module_name' id='module_name_{i}' font-size='14' y='{y}%' "
        html += f"x='{x}' >{module}</text>\n"

        #line separator
        x1 = ((subseq.end) / L) *WIDTH +x0
        html += f"<line class='separator' id='separator_{i}' y1='{y_top}%' y2='{y_top+y_height}%' stroke='black' stroke-width='2' "
        html += f"x1='{x1}' x2='{x1}' />\n"

        #text numbering
        if(i < len(Subseqs)):
            y = y_top + y_height + 5
            if(chtext):
                chtext = False
                y += (5 *chlvl)
            x = ((subseq.end) / L) *WIDTH +x0
        else:
            text_length:int = len(str(subseq.end))
            y = y_top + y_height + 10 + 5 *chlvl
            x = (real_WIDTH - text_length *10)
        html += f"<text class='numbering' id='numbering_{i}' font-size='10'  "
        html += f" y='{y}%' x='{x}' >{subseq.end}</text>\n"
    html += "</svg></div>"

    return "<div class='figure'>"+html+"</div>"


def generate_minusfigure_protein(protein:data.Protein):
    html:str = ""
    WIDTH = 1000

    organism = protein.organism
    L = len(protein.sequence)

    html += f"<div class='button-container'><button id='button_{protein.id}' onclick='makeAsReference({protein.id})' class='btn'><span class='uni_star' value=false >★</span></button>"
    html += f"<button class='plus' onclick='updateSection_figure_plus({protein.id})'>+</button></div>\n"
    html += f"<div class='svg-container'><svg protein={protein.id} width={WIDTH} height='150'>"
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

    return "<div class='figure'>"+html+"</div>"


def generate_mainfigure_profile(data:dict):
    msa:list = []   
    with open(data["outfile_path"]) as handle:
        for record in SeqIO.parse(handle, format="fasta"):
            msa.append({"header": record.description, "sequence":str(record.seq)})
    # parameters 
    N:int = len(msa)
    L:int = len(msa[0]["sequence"])
    ### html
    html:str = f"<div class='msa'>"
    ### 
    # div functional button #
    div_icons:str = "<div class='icons' ><span class='whitespace'>_</span><span class='whitespace'>_</span>"
    # div header #
    div_header:str = "<div class='headers' >"
    div_header += "<span class='residue' >Records:</span><span class='whitespace'>_</span>"
    # div graduated ruler #
    # div sequences #
    div_sequences:str = "<div >"
    # visible positions
    div_sequences += "<div class='scroll_values' ><span id='start' ></span><span id='middle' ><span class='whitespace'>_</span></span><span id='end' ></span></div>"
    div_sequences += "<div class='sequences' >"
    ruler:str = ""
    for l in range(L):
        if(l%5 == 0 and l > 0):
            ruler += f"<span pos={l} >|</span>"
        else :
            ruler += f"<span class='whitespace' pos={l} >_</span>"
    div_sequences += f"<span class='sequence' >{ruler}</span>"
    # div horizontal scroll # 

    for record in msa:
        subseq_id:str = record['header']
        subseq_id = subseq_id.split('@')[-1].split('.')[-1].split(')')[0]
        div_icons += f"<span class='sequence_selected_icon' subseq='{subseq_id}' ><span class='whitespace'>_</span></span>"
        div_header += f"<span >{record['header']}</span>"
        div_sequences += "<span class='sequence' >"
        div_sequences +=  "".join(f"<span data-residue='{residue}' class='residue' >{residue}</span>" for residue in record['sequence'])
        div_sequences += "</span>"

    div_icons += "</div>"
    div_header += "</div>"
    div_sequences += "</div></div>"

    ### 
    html += div_icons
    html += div_header
    html += div_sequences
    ### 
    html += "</div>"
    return html 


