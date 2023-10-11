from datamolo.models import *
from django.conf import settings

import re
import json

from os import path

from Bio import SeqIO, Seq



def custom_csv_parser_to_list(infilepath:str) -> list:
    with open(path.join(settings.TABLES_CSV, infilepath+".csv") ,'r') as handle:

        rows:list = []

        for line in handle.readlines():
            line = line.strip(';') # removing terminal ';' 
            values:list = [] # re-initialize value list
            val:str = "" # current parsing value
            inquote:bool = False # re-initialize in quote : False
            quote_char:str = '' # ' or "
            for c in line:
                if(c == ','): # encounter comma
                    if(not inquote): ## and not in quote
                        val = val.strip("'")
                        val = val.strip('"')
                        if(len(val) > 0):
                            values.append(val)
                        else:
                            values.append(None)
                        val = ""
                        continue
                elif(c == '"' or c == "'"): # encounter quote
                    if(inquote): # already in quote 
                        if(quote_char == c):  # encounter ending quote mark
                            inquote = False
                        else: # encounter the other quote mark 
                            pass
                    else: # encounter starting quote mark
                        inquote = True
                        quote_char = c
                elif((c == ' ' or c == '\n') and not inquote):  # get rid of whitespaces
                    continue
                val += c
            if(len(val)>0):
                val = val.strip("'")
                val = val.strip('"')
                values.append(val)

            if(len(values) > 0):
                rows.append(values)
                #print(values)  
        
        #print("nbr of col", set([len(row) for row in rows]))
        #print("nbr of rows", len(rows))
        return rows

def custom_csv_parser_to_csv(infilepath:str, id:str ) -> list:
    with open(path.join(settings.TABLES_CSV, infilepath+".csv") ,'r') as handle:

        for line in handle.readlines():
            if(line.startswith(id+",")):
                line = line.strip(';') # removing terminal ';' 
                values:list = [] # re-initialize value list
                val:str = "" # current parsing value
                inquote:bool = False # re-initialize in quote : False
                quote_char:str = '' # ' or "

                for c in line:
                    if(c == ','): # encounter comma
                        if(not inquote): ## and not in quote
                            val = val.strip("'")
                            val = val.strip('"')
                            if(len(val) > 0):
                                values.append(val)
                            else:
                                values.append(None)
                            val = ""
                            continue
                    elif(c == '"' or c == "'"): # encounter quote
                        if(inquote): # already in quote 
                            if(quote_char == c):  # encounter ending quote mark
                                inquote = False
                            else: # encounter the other quote mark 
                                pass
                        else: # encounter starting quote mark
                            inquote = True
                            quote_char = c
                    elif((c == ' ' or c == '\n') and not inquote):  # get rid of whitespaces
                        continue
                    val += c

                if(len(val)>0):
                    val = val.strip("'")
                    val = val.strip('"')
                    values.append(val)

                if(len(values) > 0):
                    return(values)
        
        return []


def Get_fastaseq_from_file(id:str) -> Seq:
    # Read the Sequences fasta file
    with open(settings.MULTIFASTA) as handle:
        for record in SeqIO.parse(handle,format="fasta"):
            if(record.id == id):
                return record.seq

def Get_name_from_CAZy_DB(id:str) -> str:
    csv = custom_csv_parser_to_csv("CAZy_DB", id)
    return csv[1]

def Get_org_name_from_CAZy_DB(id:str) -> str:
    csv = custom_csv_parser_to_csv("CAZy_DB", id)
    return csv[3]

def Get_limits_of_subseq(id:str) -> tuple:
    Compositions = custom_csv_parser_to_list("ModO_Composition")
    compo = Compositions[int(id)]
    Limits = custom_csv_parser_to_list("ModO_Limits")
    for lim in Limits:
        if(lim[0] == compo[0] and lim[1] == compo[1]):
            return (int(lim[-2]), int(lim[-1]))

def parse_data():

    # Read the DATA json file
    data:dict = {}
    with open(settings.DATA) as handle:
        data = json.load(handle)

    # Parse data dict
    ## species -> Organism__Tax_id
    for Oraganism__Tax_id in data:
        Tax_id:str = Oraganism__Tax_id

        for CAZy_DB__DB_ac in data[Oraganism__Tax_id]:
            ### data_ac -> CAZy_DB__DB_ac
            data_ac:str = CAZy_DB__DB_ac
            ### get fasta seq of CAZy_DB__DB_ac
            fastaseq:str = Get_fastaseq_from_file(CAZy_DB__DB_ac)
            ### get protein name
            name:str = Get_name_from_CAZy_DB(CAZy_DB__DB_ac)
            ### get organism name
            org_name:str = Get_org_name_from_CAZy_DB(CAZy_DB__DB_ac)
            ### create header 
            header_fasta:str = name.replace(" ", "_")+"__"+"(@"+data_ac+")"

            ### if organism doesnt exist yet 
            if(len(Organism.objects.filter(id=int(Tax_id)))<1): 
                ### add organism in MODELS (tax_id, name, phylogeny?)
                Organism_model = Organism.objects.create(
                    id = int(Tax_id),
                    name = org_name,
                    phylogeny = ""
                )
            else:
                ### if exists : will need it 
                Organism_model = Organism.objects.get(id=int(Tax_id))

            ### add protein in MODELS (Tax_id, data_ac, fastaseq, name, header)
            if(len(Protein.objects.filter(data_ac = int(data_ac)))<1):
                Protein_model = Protein.objects.create(
                    #isPP = False, 
                    #derivedFromPP = False,
                    organism = Organism_model,
                    name = name,
                    data_ac = int(data_ac),
                    header = header_fasta,
                    sequence = fastaseq
                )
            else:
                Protein_model = Protein.objects.get(data_ac = int(data_ac))

            for subseq in data[Oraganism__Tax_id][CAZy_DB__DB_ac]["subseq"]:
                ### key   -> composition_lineNumber
                ### value -> domain__id
                start, end = Get_limits_of_subseq(subseq)

                ### add subseq in MODELS (origin, profile?, start, end)
                if(len(Subseq.objects.filter(origin = Protein_model, start = int(start)))<1):
                    Subseq_model = Subseq.objects.create(
                        origin = Protein_model,
                        start = start,
                        end = end,
                        profile = None
                    )
                else:
                    Subseq_model = Subseq.objects.get(origin = Protein_model, start = int(start))

                ### Parse Modulo
                modulo_id:str = data[Oraganism__Tax_id][CAZy_DB__DB_ac]['subseq'][subseq]
                #### check if modulo_id is legit (cuz' could happend)
                if(Modulo.Do_exist(modulo_id)):
                    if(len(Modulo.objects.filter(id=modulo_id))<1): 
                        module = Modulo.objects.create(
                            id = modulo_id,
                            moduloFamily = Modulo.Get_Family(modulo_id),
                            #activity = None
                        )
                        # create Profile
                        profile = Profile.objects.create(modulo = module)
                    else:
                        module = Modulo.objects.get(id=modulo_id)
                        profile = Profile.objects.get(modulo = module)

                    # link between subseq/profile
                    Subseq_model.profile = profile
                    Subseq_model.save()
            

def parse_Annotations(Annotations_tab:list):
    
    def Fetch_Modulo(protein, start:int, end:int) -> list:
        # input: protein is Protein.object
        # method: models.objects.filter(...) && if within limits
        # return: list(modulo__id:str)
        result:list = []
        for subseq in Subseq.objects.filter(origin=protein):
            ## subseq is within start-end 
            if(subseq.start >= int(start) and subseq.end <= int(end)):
                ### yatta !
                ### get profile thus modulo name
                if(subseq.profile):
                    result.append(subseq.profile.modulo.id)
        return result
    
    def Fetch_CSV(table_name:str, nline:int) -> list:
        with open(path.join(settings.TABLES_CSV, table_name+".csv") ,'r') as handle:
            k = 0
            for line in handle.readlines():
                if(k == nline):
                    line = line.strip(';') # removing terminal ';' 
                    values:list = [] # re-initialize value list
                    val:str = "" # current parsing value
                    inquote:bool = False # re-initialize in quote : False
                    quote_char:str = '' # ' or "
                    for c in line:
                        if(c == ','): # encounter comma
                            if(not inquote): ## and not in quote
                                val = val.strip("'")
                                val = val.strip('"')
                                if(len(val) > 0):
                                    values.append(val)
                                else:
                                    values.append(None)
                                val = ""
                                continue
                        elif(c == '"' or c == "'"): # encounter quote
                            if(inquote): # already in quote 
                                if(quote_char == c):  # encounter ending quote mark
                                    inquote = False
                                else: # encounter the other quote mark 
                                    pass
                            else: # encounter starting quote mark
                                inquote = True
                                quote_char = c
                        elif((c == ' ' or c == '\n') and not inquote):  # get rid of whitespaces
                            continue
                        val += c
                    if(len(val)>0):
                        val = val.strip("'")
                        val = val.strip('"')
                        values.append(val)

                    if(len(values) > 0):
                        return(values)
                        #print(values)  
                k += 1
        return []

    def Make_Annotation(**kwargs):
        if(not "modules" in kwargs):
            return None
        l_module = kwargs["modules"]

        if(len(l_module) < 1):
            #### no match
            #### no module associated to annotation
            #### OR annotation in between two subseqs
            if(kwargs.get("error_NoMatch_txt")):
                log.write(kwargs["error_NoMatch_txt"])
        
        elif(len(l_module) > 1):
            #### multiple Matches 
            #### not sure it could happen
            if(kwargs.get("error_MultiMatch_txt")):
                log.write(kwargs["error_MultiMatch_txt"])
        
        elif(len(l_module) == 1):
            module_id = kwargs["modules"][0]
            protein = Protein.objects.get(data_ac = kwargs["CAZy_DB__DB_ac"])
            #### only one match
            Annotation.objects.create(
                modulo = Modulo.objects.get(id=module_id),
                tab = kwargs["tab"],
                data_ac = kwargs["data_ac"],
                value = kwargs["value"],  #dict(regex=csv[6], activity=csv[7], phylogeny=csv[8]),
                origin = protein ,
                start_origin = kwargs["start_origin"],
                end_origin = kwargs["end_origin"],
                start_profile = 0,
                end_profile = 0
            )

    # log 
    log = open(path.join(settings.DATA_DIR,"log.txt"), 'w')
    
    # Read the DATA json file
    data:dict = {}
    with open(settings.DATA) as handle:
        data = json.load(handle)

    for Oraganism__Tax_id in data:
        for CAZy_DB__DB_ac in data[Oraganism__Tax_id]:
            for annotation in data[Oraganism__Tax_id][CAZy_DB__DB_ac]['annotation']:
                table_name:str = annotation[0]
                nline:int = int(annotation[1])

                if(table_name in Annotations_tab):
                    ## switch case 

                    ### manualy (later) 
                    if(table_name == "Prot_Infos"):
                        csv = Fetch_CSV(table_name, nline)
                        #### ['6', '0', '1', 'Consult accession', 'VaZy 94 for HR1 and HR2 domains and VaZy 169 for HR1 stucture (PDB: 1G2C)', 'NULL']
                        ### just comments 
                        ### -> data mining
                        log.write(f"prot_info:{nline} {CAZy_DB__DB_ac}:{csv[1]}:{csv[2]} {csv[3]}")
                        pass

                    ### automatic
                    elif(table_name == "Prot_MOTIF"):
                        #### ['1', '0', '1', 'motif', '322', '336', 'F-x(4)-Y-x(3)-W-S-F-A-M-G', 'nucleocapsid', 'paramyxovirinae', 'None', 'None', 'NULL']
                        protein = Protein.objects.get(data_ac=CAZy_DB__DB_ac, derivedFromPP=False)
                        csv = Fetch_CSV("Prot_MOTIF", nline)
                        l_module = Fetch_Modulo(protein, csv[4], csv[5])
                        
                        Make_Annotation(
                            modules = l_module,
                            tab = table_name,
                            data_ac = nline,
                            value = str(dict(regex=csv[6], activity=csv[7], phylogeny=csv[8])),
                            origin = CAZy_DB__DB_ac,
                            start_origin = csv[4],
                            end_origin = csv[5],
                            error_NoMatch_txt = f"NoMatch {CAZy_DB__DB_ac}[{csv[4]}:{csv[5]}] {table_name}:{nline}\n",
                            error_MultiMatch_txt = f"MultiMatch {CAZy_DB__DB_ac}[{csv[4]}:{csv[5]}] {table_name}:{nline} ({l_module})\n"
                            )
                        
                    ### manualy (later)
                    elif(table_name == "Prot_MUT"):
                        ### ['90', '0', '1', 'S228Q; L229D', "action sur l\\'interactionN=N', 'Supressiondelaformationdelanucleocapside(aggregatsaleatoires)etdelaliaisonal\\'ARN.", 'Virology 2002 Oct 25;302(2):420-32', '12441086']
                        csv = Fetch_CSV(table_name, nline)
                        log.write(f"{table_name}:{nline} {CAZy_DB__DB_ac}:{csv[1]}:{csv[2]} {csv[3]}")
                        pass

                    ### automatic
                    elif(table_name == "Prot_REG"):
                        #13, 0, 1, 'PS', 1, 26, 'GlobPlot : 1-26=PS', 'None', 'NULL'
                        protein = Protein.objects.get(data_ac=CAZy_DB__DB_ac, derivedFromPP=False)
                        csv = Fetch_CSV("Prot_REG", nline)
                        l_module = Fetch_Modulo(protein, csv[4], csv[5])
                        Make_Annotation(
                            modules = l_module,
                            tab = table_name,
                            data_ac = nline,
                            value = str(dict(name=csv[3], description=csv[6])),
                            origin = CAZy_DB__DB_ac,
                            start_origin = csv[4],
                            end_origin = csv[5],
                            error_NoMatch_txt = f"NoMatch {CAZy_DB__DB_ac}[{csv[4]}:{csv[5]}] {table_name}:{nline}\n",
                            error_MultiMatch_txt = f"MultiMatch {CAZy_DB__DB_ac}[{csv[4]}:{csv[5]}] {table_name}:{nline} ({l_module})\n"
                            )
                        
                    ### automatic
                    elif(table_name == "Prot_RI"):
                        #6, 0, 1, 'dissulfide bridge Cys 1', 71, 71, 'None', 'name of the region with Cys 71 : F2 (in S12 module)', 'None', 'NULL'
                        protein = Protein.objects.get(data_ac=CAZy_DB__DB_ac, derivedFromPP=False)
                        csv = Fetch_CSV("Prot_RI", nline)
                        l_module = Fetch_Modulo(protein, csv[4], csv[5])
                        Make_Annotation(
                            modules = l_module,
                            tab = table_name,
                            data_ac = nline,
                            value = str(dict(name=csv[3], description=csv[7])),
                            origin = CAZy_DB__DB_ac,
                            start_origin = csv[4],
                            end_origin = csv[5],
                            error_NoMatch_txt = f"NoMatch {CAZy_DB__DB_ac}[{csv[4]}:{csv[5]}] {table_name}:{nline}\n",
                            error_MultiMatch_txt = f"MultiMatch {CAZy_DB__DB_ac}[{csv[4]}:{csv[5]}] {table_name}:{nline} ({l_module})\n"
                            )
                        
                    ### automatic
                    elif(table_name == "CAZy_GB_GP"):
                        # 1, 'NP_112021.1', 'NC_002728', '13559809', 'N', 'None', '1', 532, 'Reference'
                        # DB_ac, prot_.gb, gen_.gb, acc?, gen_name, genomic? , begin, end, ref
                        #  0   ,    1    ,   2    ,  3  ,    4    ,    5     ,   6  ,  7 ,  8
                        protein = Protein.objects.get(data_ac=CAZy_DB__DB_ac, derivedFromPP=False)
                        csv = Fetch_CSV("CAZy_GB_GP", nline)
                        l_module = Fetch_Modulo(protein, csv[6], csv[7])

                        if(len(Genome.objects.filter(organism=protein.organism)) < 1):
                            Genome.objects.create(  
                                name = csv[4],
                                genbank = csv[2],
                                organism = protein.organism
                            )

                        if(len(l_module) < 1):
                            #### no match
                            #### no module associated to annotation
                            #### OR annotation in between two subseqs
                            log.write(f"NoMatch {CAZy_DB__DB_ac}[{csv[6]}:{csv[7]}] {table_name}:{nline}\n")
                        elif(len(l_module) > 1):
                            #### multiple Matches 
                            #### not sure it could happen
                            log.write(f"MultiMatch {CAZy_DB__DB_ac}[{csv[6]}:{csv[7]}] {table_name}:{nline} ({l_module})\n")
                        elif(len(l_module) == 1):
                            #### if protein already has NOT a genbank ?
                            #### might causes pbs in CAZy_PP 
                            if(protein.genbank == ""):
                                protein.genbank = csv[1]
                                protein.save()
                            else:
                                log.write(f"AlreadyMatch {CAZy_DB__DB_ac}[{csv[6]}:{csv[7]}] {table_name}:{nline} {protein.genbank}--{csv[1]}")
                        
                    ### automatic
                    elif(table_name == "CAZy_PDB"):
                        #"DB_ac", "PDB_id", "PDB_chain", "PDB_begin", "PDB_end", "PDB_note", "PDB_bornModo"
                        #65, '1G5G', 'A', 32, 500, 'Warning: only 94.5% identity', 'S12'
                        protein = Protein.objects.get(data_ac=CAZy_DB__DB_ac, derivedFromPP=False)
                        csv = Fetch_CSV(table_name, nline)
                        l_module = Fetch_Modulo(protein, csv[3], csv[4])

                        if(len(l_module) < 1):
                            #### no match
                            #### no module associated to annotation
                            #### OR annotation in between two subseqs
                            log.write(f"NoMatch {CAZy_DB__DB_ac}[{csv[3]}:{csv[4]}] {table_name}:{nline}\n")
                        elif(len(l_module) > 1):
                            #### multiple Matches 
                            #### not sure it could happen
                            log.write(f"MultiMatch {CAZy_DB__DB_ac}[{csv[3]}:{csv[4]}] {table_name}:{nline} ({l_module})\n")
                        elif(len(l_module) == 1):
                            module = Modulo.objects.get(id=l_module[0])
                            if(len(Structure.objects.filter(id=csv[1])) < 1):
                                Structure.objects.create(
                                    id = csv[1],
                                    modulo = module,
                                    origin = Protein.objects.get(data_ac=CAZy_DB__DB_ac, derivedFromPP=False)
                                    #comment = "" (as default)
                                )
                                Annotation.objects.create(
                                    modulo = module,
                                    tab = table_name,
                                    data_ac = nline,
                                    value = str(dict(note=csv[5])),
                                    origin = protein,
                                    start_origin = csv[3],
                                    end_origin = csv[4]
                                )
                            
                    ### automatic
                    elif(table_name == "CAZy_PP"):
                        #"DB_ac", "PP_ac", "PP_gi", "PP_gene", "PP_begin", "PP_end", "PP_note", "PP_diff"
                        #268, 1, 'NP_739581', 'anchored capsid C', 1, 114, 'S98-PS', 'no'
                        # debug
                        pprotein = Protein.objects.get(data_ac=CAZy_DB__DB_ac, derivedFromPP=False)
                        csv = Fetch_CSV(table_name, nline)
                        #l_module = Fetch_Modulo(pprotein, csv[4], csv[5])

                        # to create PP 
                        pprotein.isPP = True
                        pprotein.save()

                        # to create nsp 
                        nsp = Protein.objects.create(
                            isPP = False,
                            derivedFromPP = True,
                            organism = pprotein.organism,
                            genbank = csv[2],
                            name = csv[3],
                            data_ac = CAZy_DB__DB_ac,  # no more unique ...
                            header = str(csv[3]).replace(" ", "_")+"__"+"(@"+str(csv[0])+"."+str(nline)+")",
                            sequence = pprotein.sequence[int(csv[4]):int(csv[5])]
                        )

                        PolyProtein.objects.create(
                            PP = pprotein,
                            protein = nsp,
                            index = csv[1],
                            start = csv[4],
                            end = csv[5]
                        )

                    ### automatic
                    elif(table_name == "CAZy_SP"):
                        #68, 'nucleocapsid protein', 'None', 'phocine distemper virus Ulster/88', 'PhoDisV-U88', 11240, 'None', 'None', '523', 'MASLLKSLSLFKKTREQPPLASGSGGAIRGIKHVIIVLIPGDSSIVTRSRLLDRLVRMVGDPEVSGPKLTGVLISILSLFVESPGQLIQRIIDDPDISIKLVEVIPSINSTCGLTFASRGASLDAEADEFFGTMDEGSKDHNQMGWLENKDIIDIEVNDAEQFNILLASILAQIWILLAKAVTAPDTAADSEMRRWIKYTQQRRVIGEFRMNKIWLDIVRNRIAEDLSLRRFMVALILDIKRSPGNKPRIAEMICDIDNYIVEAGLASFILTIKFGIETMYPALGLHEFSGELTTIESLMVLYQQMGETAPYMVILENSVQNKFSAGSYPLLWSYAMGVGVELENSMGGLNFGRSYFDPAYFRLGQEMVRRSAGKVSSTFAAEFGITKEEAQLVSEIVSRTTEDRTTRATGPKQSQITFLHSERNEAPNQRLPPITMKSEFQGGDKYSNQLIDDRLSGYTSDVQSSEWDESRQITQLTQEGDHDNDQQSMDGLAKMRQLTKILNQSDTNGEVSPAHNDRDLLS', 'None', '2002-05-15', '2004-03-12', 'no', 'N mononegavirales'
                        #['68', 'P35944', 'NCAP_PHODV', 'N', '1', '523', 'Reference']
                        ## simply completing Protein item
                        protein = Protein.objects.get(data_ac=CAZy_DB__DB_ac, derivedFromPP=False)
                        csv = Fetch_CSV(table_name, nline)
                        protein.genbank = csv[1]
                        protein.save()
                        pass
        
    log.close()



