import re, os, json
import Bio
import numpy as np
import subprocess as sh

from django.conf import settings

from Bio import Entrez
Entrez.email = "VIMVer@univ-amu.fr"
data_1_path:str = settings.TABLES_CSV
data_2_path:str = settings.DATA_DIR

# 
def write_Protein(Proteins):
    outfile = os.path.join(settings.DATA_DIR,"Protein.temp.json")

    with open(outfile, 'w') as handle:
        txt:list = list([json.dumps(Protein.serialize()) for Protein in Proteins])
        handle.write('[\n'+ ',\n'.join(txt) + ']')
        
def write_Modulo(Moduli):
    outfile = os.path.join(settings.DATA_DIR,"Modulo.temp.json")

    with open(outfile, 'w') as handle:
        txt:list = list([json.dumps(Modulo.serialize()) for Modulo in Moduli])
        handle.write('[\n'+ ',\n'.join(txt) + ']')
      
def write_Organism(Organisms):
    outfile = os.path.join(settings.DATA_DIR,"Organism.temp.json")

    with open(outfile, 'w') as handle:
        txt:list = list([json.dumps(org.serialize()) for org in Organisms])
        handle.write('[\n'+ ',\n'.join(txt) + ']')


def read_data_1(filename:str):
    with open(os.path.join(data_1_path, filename+".csv")) as handle:
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
      
def read_data_2(filename:str):
    with open(os.path.join(data_2_path, filename+".json")) as handle:
        return json.loads(handle.read())


def run_taxonkit(taxid:str) -> str:
    # return html content
    var = sh.run(["taxonkit","list", "--show-rank", "--show-name", "--indent", "    ", "--ids", taxid, "-J"], stdout=sh.PIPE, stderr=sh.PIPE, text=True)
    var_json = json.loads(var.stdout)

    def json2html(data:dict) -> str:
        #recursive
        txt:str = ""
        for line, subdata in data.items():
            line:str = line.strip()
            txt += "<li>"+line+"</li>"
            
            if len(subdata) > 0: #sub_clade
                txt += "<ul>" + json2html(subdata) + "</ul>"
        return txt

    return "<ul>"+json2html(var_json)+"</ul>"


def parse_vazy_data_1(Vazy1:dict) -> str:
    text:str = "<p>VaZyMolO.data 1</p>"
    for key, item in Vazy1.items():
        text += "<p>"+key+"</p>"
        text += "<ul>"
        for value in item:
            text += "<li>"+str(value)+"</li>"
        text += "</ul>"
    
    return text
