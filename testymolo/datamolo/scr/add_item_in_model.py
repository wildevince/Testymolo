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

def parse_Modules():

    # Read the DATA json file
    data:dict = {}
    with open(settings.DATA) as handle:
        data = json.load(handle)
    #
    for Oraganism__Tax_id in data:
        for CAZy_DB__DB_ac in data[Oraganism__Tax_id]:
            for subseq in data[Oraganism__Tax_id][CAZy_DB__DB_ac]['subseq']:
                modulo_id:str = data[Oraganism__Tax_id][CAZy_DB__DB_ac]['subseq'][subseq]
                if(len(Modulo.objects.filter(id=modulo_id))<1): 
                    Modulo.objects.create(
                        id = modulo_id,
                        moduloFamily = Modulo.Get_Family(modulo_id),
                        #activity = None
                    )
                

