import datamolo.models as data

from Bio import SeqIO
import logomaker as logo
import os

from django.conf import settings


### not used (old) --> generate_mainfigure_profile
def generate_mainfigure_protein_old(protein:data.Protein):
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
        lenseq = len(protein.sequence[subseq.start-1:subseq.end])
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

def generate_mainfigure_profile_old(data:dict):
    msa:list = []   
    with open(data["outfile_path"]) as handle:
        for record in SeqIO.parse(handle, format="fasta"):
            msa.append({"header": record.description, "sequence":str(record.seq)})
    # parameters 
    N:int = len(msa) #number of sequences
    L:int = len(msa[0]["sequence"]) #length of alignment
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
    div_sequences += f"<div class='scroll_values' ><span id='start' >1</span><span id='middle' ><span class='whitespace'>_</span></span><span id='end' >{L}</span></div>"
    div_sequences += "<div class='sequences' >"
    ruler:str = ""
    for l in range(L):
        l += 1
        #title = position => read as caption on mouseover
        if(l%10 == 0):
            ruler += f"<span title={l} >|</span>"
        elif(l%5 == 0):
            ruler += f"<span title={l} >-</span>"
        else :
            ruler += f"<span class='whitespace' title={l} >_</span>"
    div_sequences += f"<span class='sequence' >{ruler}</span>"
    # div horizontal scroll # 

    for record in msa:
        subseq_id:str = record['header']
        subseq_id = subseq_id.split('@')[-1].split('.')[-1].split(')')[0]
        div_icons += f"<span class='sequence_selected_icon' subseq='{subseq_id}' ><span class='whitespace'>_</span></span>"
        div_header += f"<span class='header' subseq='{subseq_id}' >{record['header']}</span>"
        div_sequences += f"<span class='sequence' subseq='{subseq_id}' >"
        n = 1 #aligned position => read as caption when mouseovered 
        p = 0 #real position
        for residue in record['sequence']:
            if(residue != '-'): #if not a gap
                p += 1
            div_sequences +=  f"<span class='residue' data-residue='{residue}' realpos='{p}' alignedpos='{n}' title='{p}-{n}' >{residue}</span>"
            n += 1
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


# LastCommonAncestor
def LastCommonAncestor(phylos:list) -> str:
    def AllSameStrings(strings:list) -> bool:
        if len(strings) > 1:
            item = strings[0]
            for w in strings[1:]:
                if item != w :
                    return False
            return True
        else:
            return False
        
    N = min([len(k) for k in phylos])
    if N > 0:
        lastCommonAncestor = ""
        for k in range(N):
            if AllSameStrings([phylo[k] for phylo in phylos]):
                lastCommonAncestor = phylos[0][k]
    return lastCommonAncestor


####################################################
### profile - version 2.0
class Profile:
    
    def __init__(self, filepath:str, method:str) -> None:
        msa:list = []
        with open(filepath) as handle:
            for record in SeqIO.parse(handle, format='fasta'):
                msa.append({'header': record.description, 'sequence':str(record.seq)})
        self.N:int = len(msa) #number of sequences
        self.L:int = len(msa[0]["sequence"]) #length of alignment
        self.ruler:list = []
        for l in range(self.L):
            l += 1
            if(l%10 == 0):
                self.ruler.append({'i':l, 'v':'|'})
            elif(l%5 == 0):
                self.ruler.append({'i':l, 'v':'-'})
            else:
                self.ruler.append({'i':l, 'v':'_'})
        
        # MSA
        self.icons:list = []
        self.origin:list = []
        self.headers:list = []
        self.profile:list = []
        for record in msa:
            subseq_id:str = record['header']
            if method == 'OnTheFly':
                subseq_id = subseq_id.split('@')[-1].split('.')[-1].split(')')[0]
            elif method == 'Aligned':
                subseq_id = subseq_id.split('.')[2]
            origin = data.Subseq.objects.get(id=int(subseq_id)).origin.organism
            sequence:list = []
            p = 0  # real position
            for n in range(1, len(record['sequence'])+1):  # aligned position
                residue = record['sequence'][n-1]
                if residue != '-':  # is not gap
                    p += 1
                sequence.append({'residue':residue, 'realPos':p, 'alignedPos':n})
            
            self.icons.append({'id':subseq_id})
            self.origin.append({'taxid':origin.id, 'abr':origin.abr})
            self.headers.append({'id':subseq_id, 'header':record['header']})
            self.profile.append({'id':subseq_id, 'sequence':sequence})

    def Display(self):
        return {'ruler': self.ruler, 'L': self.L, 'icons':self.icons, 'origin':self.origin, 'headers':self.headers, 'profile':self.profile}
        
def generate_mainfigure_profile(outfile_path:str, method:str):
    print("generate_mainfigure_profile --version 2.0")
    profile = Profile(outfile_path, method)
    return profile.Display()
    

##########################################################################################################################
### main figure version 2.0
class Figure():
    Templates:list = {'protein':''}
    TRUE_WIDTH:int = 1890  # [pixel]
    WIDTH:int = 1780  # [pixel]
    x0:int = 12  # x_offset  [pixel]
    y0 = 75  # y_offset  [pixel]
    h0 = 40  # feature height  [pixel]
    h1 = 80  # between feature height  [pixel]

    def __init__(self, protein:data.Protein, showhide_allnsp:bool=False) -> None:
        """ return HTML content """
        self.inputdata = Figure.formating_inputdata(protein)
        self.PP = self.inputdata[0]
        self.HEIGHT = Figure.y0  # [pixel] 
        self.solo:bool = True if len(self.inputdata) == 0 else False
        if showhide_allnsp:
            N:int = len(self.inputdata)
        else:
            N:int = len([p for p in self.inputdata if len(p['subseq']) > 0]) 
            N:int = 2 if N > 1 else 1
        self.HEIGHT += N*(Figure.h0 + Figure.h1)  # [pixel]
        self.HTML_data:dict = {}

        self.HTML_data['protein_header'] = self.PP['header']
        self.HTML_data['id'] = self.PP['id']
        self.HTML_data['Width'] = str(Figure.TRUE_WIDTH)
        self.HTML_data['Height'] = str(self.HEIGHT)
    
        # Organism
        org = data.Organism.objects.get(id=self.PP['organism'])
        self.HTML_data['Org'] = {'x':Figure.x0 +5, 'y':14, 'name':org.name, 'id':org.id}

        self.HTML_data['Protein'] = [self.Protein(0)]

        if self.PP['isPP']:

            for protein_i in range(1, len(self.inputdata)):
                if ((not showhide_allnsp) and (len(self.inputdata[protein_i]['subseq']) > 0)) :
                    self.HTML_data['Protein'].append(self.Protein(protein_i, 1))
                elif showhide_allnsp:
                    self.HTML_data['Protein'].append(self.Protein(protein_i, protein_i))
        
    def Protein(self, i:int, n:int=0) -> dict:
        protein = self.inputdata[i]
        html:dict = {}
        html['i'] = i
        html['n'] = n

        xi = Figure.x0  # x_offset 
        xi += ((protein['start']-1) / self.PP['length']) * Figure.WIDTH  # + relative position from PP
        yi = Figure.y0 + (n) * (Figure.h0 + Figure.h1)   # as downwards as many proteins to display
        wi = (protein['length'] / self.PP['length']) * Figure.WIDTH  # adjust width with length protein
        hi = Figure.h0

        #dotted line for nsps
        if n > 0:
            x_bl1 = xi
            y_bl1 = Figure.x0 -30
            x_bl2 = x_bl1
            y_bl2 = yi + hi + 30
            html['x_bl1'] = x_bl1
            html['y_bl1'] = y_bl1
            html['x_bl2'] = x_bl2
            html['y_bl2'] = y_bl2

        #protein name
        x_txt = xi +5
        y_txt = yi -32
        html['name'] = protein['name']
        html['x_txt'] = x_txt
        html['y_txt'] = y_txt

        #protein rect
        html['xi'] = xi
        html['yi'] = yi
        html['wi'] = wi
        html['hi'] = hi

        chtext:bool = False
        chlvl:int = 0

        html['subseq'] = []
        for sseq_i in range(len(protein['subseq'])):
            html['subseq'].append(self.Subseq(protein, sseq_i, xi, yi, wi, hi, chtext, chlvl))
            #pass

        return html

    def Subseq(self, protein, j, *coord) -> dict:
        subseq = protein['subseq'][j]
        xi, yi, wi, hi, chtext, chlvl, *_ = coord
        html:dict = {}

        L = len(protein['sequence'])
        len_sseq:int = len(protein['sequence'][subseq['start']-1:subseq['end']])

        xj = xi
        #if protein['isPP'] or (not protein['isPP'] and not protein['derivedFromPP']):
        xj += ((subseq['start']-1)/L *wi)
        #print(subseq['start'] , L, xi, xj)
        yj = yi
        wj = ((len_sseq +1) / L) *wi
        hj = hi

        html['j'] = j
        html['id'] = subseq['id']
        html['xj'] = xj
        html['yj'] = yj
        html['wj'] = wj
        html['hj'] = hj
        
    
        if(wj < (0.022 *Figure.WIDTH)):
            chtext = True
            chlvl += 1  
        else:
            chlvl = chlvl-1 if(chlvl > 0) else 0

        # text module_name
        x_mod = xj
        y_mod = yj
        if(wj > (0.022 *Figure.WIDTH)):
            x_mod += wj*2/5
        y_mod -= 5
        if(chtext):
            y_mod -= (12 *chlvl)

        html['mod_id'] = subseq['modulo']['id']
        html['x_mod'] = x_mod
        html['y_mod'] = y_mod

        #line separator
        #x_sep1 = (subseq['end'] / L) *wi +xi 
        x_sep1 = xj + wj
        y_sep1 = yi
        x_sep2 = x_sep1
        y_sep2 = y_sep1 + Figure.h0
        html['x_sep1'] = x_sep1
        html['y_sep1'] = y_sep1
        html['x_sep2'] = x_sep2
        html['y_sep2'] = y_sep2

        #text numbering
        x_numb = x_sep1
        y_numb = yi + Figure.h0 + 15
        if(chtext):
            chtext = False
            y_numb += (12 *chlvl)
        html['x_numb'] = x_numb
        html['y_numb'] = y_numb
        html['end'] = subseq['end']

        html['color'] = 'blue'
        if subseq['modulo']['id'] in ['TM', 'UNK', 'NF', 'PS', 'LNK', '?', None, 'null', '']:  #if unimportant module
            html['color'] = 'grey'
        elif protein['complete'] and subseq['modulo']['complete'] :  # protein and modulo complete
            html['color'] = 'green'
        elif protein['complete'] or subseq['modulo']['complete']:  # protein or modulo complete
            html['color'] = 'teal'
        
        return html

    def Display(self):
        return self.HTML_data

    def formating_inputdata(protein:data.Protein) -> list:
        #data:list = []
        ##META## 
        # if len(data) == 1 : une protein
        # if len(data) > 1 : 1er->
            # -> proteins :dict
                # \-> { **prot, 'subseq':[{ **sseq, 'modulo':mod }] }
        inputdata:list = [protein.serialize(start=1)]
        solo_nsp:bool = False
        if protein.isPP:
            nsps = [nsp.serialize() for nsp in protein.get_all_nsps()]
            inputdata = [*inputdata, *nsps]
        else:  # protein.derivedFromPP:
            solo_nsp = True

        for i in range(len(inputdata)):
            inputdata[i]['subseq'] = []

            for item in data.PolyProtein.objects.filter(protein=inputdata[i]['id']):
                if not solo_nsp:
                    inputdata[i]['start'] = item.start
                else:
                    inputdata[i]['start'] = 1
                break

            for sseq in data.Subseq.objects.filter(origin=inputdata[i]['id']):
                mod_id = sseq.profile.modulo.id  # get modulo.id
                print(mod_id)
                mod_data = sseq.profile.modulo.serialize()  # serialize modulo
                sseq_data = sseq.serialize()  # serialize subseq
                sseq_data['modulo'] = mod_data  # replace modulo item
                inputdata[i]['subseq'].append(sseq_data)  # append to DATA
                """try:
                    inputdata[i]['subseq'].append(sseq.serialize(modulo=sseq.profile.modulo.serialize()))
                except :
                    inputdata[i]['subseq'].append(sseq.serialize(modulo={'id':'?'}))"""
        #print(inputdata)
        return inputdata

def generate_mainfigure_protein(protein:data.Protein, showhide_allnsp:bool=False) -> dict:   
    figure = Figure(protein, showhide_allnsp)
    return figure.Display()



