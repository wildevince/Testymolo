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
        
        print("nbr of col", set([len(row) for row in rows]))
        print("nbr of rows", len(rows))
        return rows

def Get_fastaseq_from_file(id:str) -> Seq:
    # Read the Sequences fasta file
    with open(settings.MULTIFASTA) as handle:
        for record in SeqIO.parse(handle,format="fasta"):
            if(record.id == id):
                return record.seq

def Get_name_from_CAZy_DB(id:str) -> str:
    CAZy_DB = custom_csv_parser_to_list("CAZy_DB")
    for item in CAZy_DB:
        if(item[0] == id) :
            return item[1]

def Get_org_name_from_CAZy_DB(id:str) -> str:
    CAZy_DB = custom_csv_parser_to_list("CAZy_DB")
    for item in CAZy_DB:
        if(item[0] == id) :
            return item[3]

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

            ### organism doesnt exist yet 
            if(len(Organism.objects.filter(id=int(Tax_id)))<1): 
                ### add organism in MODELS (tax_id, name, phylogeny?)
                Organism_model = Organism.objects.create(
                    id = int(Tax_id),
                    name = org_name,
                    phylogeny = ""
                )
            else:
                Organism_model = Organism.objects.get(id=int(Tax_id))

            ### add protein in MODELS (Tax_id, data_ac, fastaseq, name, header)
            if(len(Protein.objects.filter(data_ac = int(data_ac)))<1):
                Protein_model = Protein.objects.create(
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

          

def parse_Annotations():
    #
    def Fetch_Modulo(protein, start:int, end:int) -> list:
        # input: protein is Protein.object
        # method: models.objects.filter(...)
        # return: list(modulo__id:str)
        result:list = []
        for subseq in Subseq.objects.filter(origin=protein):
            ## subseq is within start-end 
            if(subseq.start >= start and subseq.end <= end):
                ### yatta !
                ### get profile thus modulo name
                if(subseq.profile):
                    result.append(subseq.profile.modulo.id)
    
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
        return []

    def Make_Annotation(**kwargs):
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

                ## switch case 
                if(table_name == "Prot_Infos"):
                    #### ['6', '0', '1', 'Consult accession', 'VaZy 94 for HR1 and HR2 domains and VaZy 169 for HR1 stucture (PDB: 1G2C)', 'NULL']
                    ### just comments 
                    ### -> data mining
                    """
                    Annotation.objects.create(
                        #modulo = Modulo.objects.get(id=),
                        tab = table_name,
                        data_ca = nline,
                        #value = CSV.[4],
                        origin = Protein.objects.get(data_ac = CAZy_DB__DB_ac),
                        start_origin = 1
                        #end_origin = len(Subseq.objects.get().sequence),
                        start_profile = 0, 
                        end_profile = 0
                    )"""
                    pass
                elif(table_name == "Prot_MOTIF"):
                    #### ['1', '0', '1', 'motif', '322', '336', 'F-x(4)-Y-x(3)-W-S-F-A-M-G', 'nucleocapsid', 'paramyxovirinae', 'None', 'None', 'NULL']
                    protein = Protein.objects.get(data_ac=CAZy_DB__DB_ac)
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
                        error_MultiMatch_txt = f"MultiMatch {CAZy_DB__DB_ac}[{csv[4]}:{csv[5]}] {table_name}:{nline} ({', '.join(l_module)})\n"
                        )
                    
                elif(table_name == "Prot_MUT"):
                    ### ['90', '0', '1', 'S228Q; L229D', "action sur l\\'interactionN=N', 'Supressiondelaformationdelanucleocapside(aggregatsaleatoires)etdelaliaisonal\\'ARN.", 'Virology 2002 Oct 25;302(2):420-32', '12441086']
                    pass
                elif(table_name == "Prot_REG"):
                    pass
                elif(table_name == "Prot_RI"):
                    pass
                elif(table_name == "CAZy_GB_GP"):
                    pass
                elif(table_name == "CAZy_PDB"):
                    pass
                elif(table_name == "CAZy_PP"):
                    pass
                elif(table_name == "CAZy_SP"):
                    pass
    
    log.close()